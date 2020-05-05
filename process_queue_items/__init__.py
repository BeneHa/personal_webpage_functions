import logging
import json
import uuid
import os
import requests

import azure.functions as func


def main(msg: func.QueueMessage, processedRequests: func.Out[str], outMail: func.Out[str]) -> None:
    logging.info(f"Python queue trigger function started")
    message_body = msg.get_body().decode("utf-8")

    #Process message, write to BLOB table store
    msg_dict = json.loads(message_body)

    #Get information about the IP
    ipstack_api_key = os.environ["ipstack_api_key"]
    ip_information = requests.post(f"http://api.ipstack.com/{msg_dict['ip_address']}?access_key={ipstack_api_key}")
    res = ip_information.json()

    logging.info(f"IP information resolved at ipstack: {res}")

    rowKey = str(uuid.uuid4())
    msg_dict["rowKey"] = rowKey
    msg_dict["browser"] = f"{msg_dict['browser_name']}, version {msg_dict['browser_version']}"
    msg_dict["os"] = f"{msg_dict['os_name']}, version {msg_dict['os_version']}"
    msg_dict["country_name"] = res["country_name"]
    msg_dict["region_name"] = res["region_name"]
    msg_dict["city"] = res["city"]
    
    #Partition by Country, fill if no country is given
    msg_dict["partitionKey"] = msg_dict["country_name"] if msg_dict["country_name"] is not None else "unidentified"

    #Delete combined fields
    for nam in ["browser_name", "browser_version", "os_name", "os_version"]:
        del msg_dict[nam]

    processedRequests.set(json.dumps(msg_dict))
    logging.info(f"Request {str(msg_dict)} was written to output table.")
