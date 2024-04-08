import logging
import json

import pandas as pd
import numpy as np

from celery import shared_task

from rpy2.rinterface_lib.sexp import NACharacterType

from ohdsi.sqlrender import read_sql, render, translate
from ohdsi.database_connector import query_sql
from ohdsi.common import convert_from_r

from . import OHDSITask

log = logging.getLogger(__name__)


@shared_task(bind=True, ignore_result=False, time_limit=60, base=OHDSITask)
def query_standard_features(
    self,
    condition_concept_ids: list[int] = None,
    procedure_concept_ids: list[int] = None,
    measurement_concept_ids: list[int] = None,
    drug_concept_ids: list[int] = None,
) -> pd.DataFrame | bool:

    log.info("Querying basic data set")

    log.debug("Reading SQL from file")
    try:
        sql = read_sql("/app/api/task/data/standard_features.sql")
    except Exception as e:
        log.exception(e)
        return {"error": "Could not read SQL from file", "exception": str(e)}

    log.debug("Rendering SQL")
    condition_concept_ids = (
        ["NULL"] if condition_concept_ids is None else condition_concept_ids
    )
    procedure_concept_ids = (
        ["NULL"] if procedure_concept_ids is None else procedure_concept_ids
    )
    measurement_concept_ids = (
        ["NULL"] if measurement_concept_ids is None else measurement_concept_ids
    )
    drug_concept_ids = ["NULL"] if drug_concept_ids is None else drug_concept_ids
    sql = render(
        sql,
        cohort_table=f"{self.request.result_schema}.allpatients",
        cohort_id=12700000,
        cdm_database_schema=self.request.schema,
        incl_condition_concept_id=condition_concept_ids,
        incl_procedure_concept_id=procedure_concept_ids,  # 4066543
        incl_measurement_concept_id=measurement_concept_ids,
        incl_drug_concept_id=drug_concept_ids,  #'ALL' ? @TODO in algo
    )

    log.debug("Translating SQL to target dialect")
    sql = translate(sql, target_dialect=self.request.dbms)

    log.debug("Executing SQL")
    try:
        result = query_sql(self.request.connection, sql)
    except Exception as e:
        with open("/app/errorReportSql.txt", "r") as f:
            error_report = f.read()
        return {"error": str(error_report)}

    log.debug("Load from R object")
    df = convert_from_r(result)

    df["OBSERVATION_VAS"] = df["OBSERVATION_VAS"].apply(
        lambda val: np.nan if isinstance(val, NACharacterType) else val
    )

    # We could have multiple observations per patient, so we need to aggregate them
    # for now we simply pick the first observation
    sub_df = df.drop_duplicates("SUBJECT_ID", keep="first")

    # print how many rows we have dropped
    log.info(f"Dropped {len(df) - len(sub_df)} rows")

    return sub_df
