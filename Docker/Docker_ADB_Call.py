# Databricks notebook source
#pip install databricks_api

# COMMAND ----------

import requests
import json
from databricks_api import DatabricksAPI
import sys
import ast

def databricks_post_request(API_Databricks_arg1="['customer']"):

    token = 'ADD THE TOKEN HERE'
    db = DatabricksAPI(
        host="ADD THE LINK HERE",
        token=token
    )
    job_payload = {
        "run_name": 'just_a_run',
        "existing_cluster_id": '0423-212957-vl2qhpwd',
        "notebook_task":
            {
                "notebook_path": '/Shared/MetaDatarepliaction_Backend_Code/Modular_Replication_Code',
                "base_parameters": {"list1": API_Databricks_arg1}

            }
    }
    resp = requests.post('ADD THE LINK HERE',
                         json=job_payload, headers={'Authorization': 'Bearer ' + token})
    run_id = int(resp.text[10:-1])
    final_result = db.jobs.get_run_output(run_id=run_id)
    print(final_result, job_payload)



if __name__=="__main__":
    API_Databricks_arg1 = ast.literal_eval(sys.argv[1])
    databricks_post_request(str(API_Databricks_arg1))









