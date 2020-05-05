import logging
import json

import azure.functions as func


def main(req: func.HttpRequest, outputQueue: func.Out[func.QueueMessage]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    #Check if body is a valid JSON
    try:
        req_body = req.get_json()
    except ValueError:
        logging.info("No valid JSON in request body.")
        return func.HttpResponse(
            "Please pass data in valid JSON format.",
            status_code = 400
        )

    #Check if all necessary arguments are given in body
    req_page = req_body.get("page_name")
    req_browser_name = req_body.get("browser_name")
    req_browser_version = req_body.get("browser_version")
    req_os_name = req_body.get("os_name")
    req_os_version = req_body.get("os_version")
    req_device = req_body.get("device")
    req_ip = req_body.get("ip_address")

    args = [req_page, req_browser_name, req_browser_version, req_os_name, req_os_version, req_device, req_ip]
    arg_names = ["req_page", "req_browser_name", "req_browser_version", "req_os_name", "req_os_version", "req_device", "req_ip"]
    missing_arg_positions = [i for i, x in enumerate(args) if x is None]
    missing_arg_names = [arg_names[pos] for pos in missing_arg_positions]

    if len(missing_arg_names) > 0:
        logging.info(f"Exiting due to missing values {str(missing_arg_names)}")
        return func.HttpResponse(
            f"Please include the missing argument(s) {str(missing_arg_names)} in the request JSON",
            status_code=400
        )
    else:
        logging.info(f"Correct values provided for all fields.")

    #TODO: check if extra fields are given

    outputQueue.set(json.dumps(req_body))
    logging.info(f"New row was entered in output queue for {req_body}")
    return func.HttpResponse(f"Request processed successfully")