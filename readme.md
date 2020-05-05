# Processing webpage visits

This project consists of three Azure functions used for tracking visitors to my [webpage](https://github.com/BeneHa/personal_webpage) (not because this is the obvious way but because I wanted to try out Azure Functions).

The first one, http_trigger_page_visit, exposes a HTTP endpoint and gets sent all tracking information that Django extracts. It writes this information to an Azure storage queue for processing.

The second one, process_queue_items, watches the queue, takes new queue entries and enriches their data (calling the IPStack API to get location data belonging to the IP on a city level). It then writes the entry to an Azure BLOB table.

The third one, regular-storage_report, sends me a daily mail informing me about the visitors on my page in the last 24 hours.