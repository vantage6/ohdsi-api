import logging
import json

import pandas as pd

from celery import shared_task

from ohdsi.common import convert_to_r
from ohdsi.cohort_generator import (
    generate_cohort_set,
    get_cohort_table_names,
    create_cohort_tables,
)
from ohdsi.circe import (
    cohort_expression_from_json,
    create_generate_options,
    build_cohort_query,
)


from . import OHDSITask

log = logging.getLogger(__name__)


def create_cohort_query(cohort_definition: dict) -> str:
    """
    Creates a cohort query from a cohort definition in JSON format.

    Parameters
    ----------
    cohort_definition: dict
        The cohort definition in JSON format, for example created from ATLAS.

    Returns
    -------
    str
        The cohort query.
    """
    cohort_expression = cohort_expression_from_json(cohort_definition)
    options = create_generate_options(generate_stats=True)
    return build_cohort_query(cohort_expression, options)[0]


@shared_task(bind=True, ignore_result=False, time_limit=60, base=OHDSITask)
def create_all_patients_cohort(self) -> bool:

    log.info("Creating all patients cohort")
    cohort_table = f"allpatients"
    cohort_id = 12700000

    # Read cohort definition from JSON
    log.debug("Reading cohort definition from JSON")
    try:
        with open("/app/api/task/data/allPatients.json", "r") as f:
            cohort_definition = json.load(f)
    except Exception as e:
        log.exception(e)
        return {
            "error": "Could not read cohort definition from JSON",
            "exception": str(e),
        }

    log.debug("Creating cohort query")
    try:
        cohort_query = create_cohort_query(cohort_definition)
        cohort_definition_set = pd.DataFrame(
            {
                "cohortId": [cohort_id],
                "cohortName": ["allPatients"],
                "json": [cohort_definition],
                "sql": [cohort_query],
                "logicDescription": [None],
                "generateStats": [True],
            }
        )
    except Exception as e:
        log.exception(e)
        return {
            "error": "Could not create cohort query",
            "exception": str(e),
        }

    # convert cohort_definition_set to R object so it can be read by the OHDSI cohort
    # generator
    cohort_definition_set = convert_to_r(cohort_definition_set)

    cohort_table_names = get_cohort_table_names(cohort_table)
    log.debug(f"Cohort table names: {cohort_table_names}")

    log.debug("Creating cohort tables in database")
    log.debug(self.request.connection)
    try:
        create_cohort_tables(
            connection=self.request.connection,
            cohort_database_schema=self.request.result_schema,
            cohort_table_names=cohort_table_names,
        )
        log.debug("Cohort tables created")
    except Exception as e:
        with open("/app/errorReportSql.txt", "r") as f:
            error_report = f.read()
        log.exception(e)
        return {
            "error": "Could not create cohort tables",
            "exception": str(e),
            "error_report": error_report,
        }

    log.debug("Generating cohort set")
    try:
        generate_cohort_set(
            connection=self.request.connection,
            cdm_database_schema=self.request.schema,
            cohort_database_schema=self.request.result_schema,
            cohort_table_names=cohort_table_names,
            cohort_definition_set=cohort_definition_set,
        )
        log.debug("Cohort set generated")
    except Exception as e:
        with open("/app/errorReportSql.txt", "r") as f:
            error_report = f.read()
        log.exception(e)
        return {
            "error": "Could not create cohort tables",
            "exception": str(e),
            "error_report": error_report,
        }

    log.info("All patients cohort created")
    return True
