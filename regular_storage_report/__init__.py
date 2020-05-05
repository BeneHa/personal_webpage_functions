import datetime
import logging
import os
import json

import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService


def main(mytimer: func.TimerRequest, sendgrid: func.Out[str]) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()    
    
    
    table_service = TableService(account_name='bhaeusewebpagefunctions', account_key=os.environ["blob_key"])

    query_timestamp = (datetime.datetime.now() + datetime.timedelta(days = -1)).strftime("%Y-%m-%dT%H:%M:%S")
    items = table_service.query_entities('processedRequests', filter= f"Timestamp ge datetime'{query_timestamp}'")
    items = list(items)

    email_text = f"""You had the following visitors: \n
                {str(items)}"""


    #Send email notification
    message = {
        "subject": f"You had {len(items)} visits on your web page!",
        "content": [{
                "type": "text/plain",
                "value": email_text }]}
        

    sendgrid.set(json.dumps(message))
    logging.info(f"Email was sent with content {email_text}")
