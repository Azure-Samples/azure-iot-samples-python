# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
This sample demonstrates how to use the Microsoft Azure Event Hubs Client for Python sync API to 
read messages sent from a device. Please see the documentation for @azure/event-hubs package
for more details at https://pypi.org/project/azure-eventhub/

For an example that uses checkpointing, follow up this sample with the sample in the 
azure-eventhub-checkpointstoreblob package on GitHub at the following link:

https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/eventhub/azure-eventhub-checkpointstoreblob/samples/receive_events_using_checkpoint_store.py
"""


from ast import While
from azure.eventhub import TransportType
from azure.eventhub import EventHubConsumerClient
import threading
import time

# Event Hub-compatible endpoint
# az iot hub show --query properties.eventHubEndpoints.events.endpoint --name {your IoT Hub name}
EVENTHUB_COMPATIBLE_ENDPOINT = "{your Event Hubs compatible endpoint}"

# Event Hub-compatible name
# az iot hub show --query properties.eventHubEndpoints.events.path --name {your IoT Hub name}
EVENTHUB_COMPATIBLE_PATH = "{your Event Hubs compatible name}"

# Primary key for the "service" policy to read messages
# az iot hub policy show --name service --query primaryKey --hub-name {your IoT Hub name}
IOTHUB_SAS_KEY = "{your service primary key}"

# If you have access to the Event Hub-compatible connection string from the Azure portal, then
# you can skip the Azure CLI commands above, and assign the connection string directly here.
CONNECTION_STR = f'Endpoint={EVENTHUB_COMPATIBLE_ENDPOINT}/;SharedAccessKeyName=service;SharedAccessKey={IOTHUB_SAS_KEY};EntityPath={EVENTHUB_COMPATIBLE_PATH}'

# Define callbacks to process events
def on_event(partition_context, event):
        print("Telemetry received: ", event.body_as_str())

def main():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group="$default",
        # transport_type=TransportType.AmqpOverWebsocket,  # uncomment it if you want to use web socket
        # http_proxy={  # uncomment if you want to use proxy 
        #     'proxy_hostname': '127.0.0.1',  # proxy hostname.
        #     'proxy_port': 3128,  # proxy port.
        #     'username': '<proxy user name>',
        #     'password': '<proxy password>'
        # }
    )
    ConsumerThread = threading.Thread(
        target=client.receive,
        kwargs={
            "on_event": on_event
        }
    )
    ConsumerThread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()
        print("Receiving has stopped.")

if __name__ == '__main__':
    main()
