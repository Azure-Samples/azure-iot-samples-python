# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
This sample demonstrates how to use the Microsoft Azure Event Hubs Client for Python async API to 
read messages sent from a device. Please see the documentation for @azure/event-hubs package
for more details at https://pypi.org/project/azure-eventhub/

For an example that uses checkpointing, follow up this sample with the sample in the 
azure-eventhub-checkpointstoreblob package on GitHub at the following link:

https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/eventhub/azure-eventhub-checkpointstoreblob-aio/samples/receive_events_using_checkpoint_store_async.py
"""


import asyncio
from azure.eventhub import TransportType
from azure.eventhub.aio import EventHubConsumerClient


# Event Hub-compatible endpoint
# az iot hub show --query properties.eventHubEndpoints.events.endpoint --name {your IoT Hub name}
EVENTHUB_COMPATIBLE_ENDPOINT = "{your Event Hubs compatible endpoint}"
EVENTHUB_COMPATIBLE_ENDPOINT = "iothub-ns-yijun-ioth-3130889-4398262da5.servicebus.windows.net"

# Event Hub-compatible name
# az iot hub show --query properties.eventHubEndpoints.events.path --name {your IoT Hub name}
EVENTHUB_COMPATIBLE_PATH = "{your Event Hubs compatible name}"
EVENTHUB_COMPATIBLE_PATH = "yijun-iothub"

# Primary key for the "service" policy to read messages
# az iot hub policy show --name service --query primaryKey --hub-name {your IoT Hub name}
IOTHUB_SAS_KEY = "{your service primary key}"
IOTHUB_SAS_KEY = "3FQcB8ptGd3QSgcq7vmNwCnRwqCZA4s+Wd2zziBKjaw="

# If you have access to the Event Hub-compatible connection string from the Azure portal, then
# you can skip the Azure CLI commands above, and assign the connection string directly here.
CONNECTION_STR = f'Endpoint=sb://{EVENTHUB_COMPATIBLE_ENDPOINT}/;SharedAccessKeyName=service;SharedAccessKey={IOTHUB_SAS_KEY};EntityPath={EVENTHUB_COMPATIBLE_PATH}';

# Define callbacks to process events
async def on_event_batch(partition_context, events):
    for event in events:
        print("Received event from partition: {}.".format(partition_context.partition_id))
        print("Telemetry received: ", event.body_as_str())
        print("Properties (set by device): ", event.properties)
        print("System properties (set by IoT Hub): ", event.system_properties)
    await partition_context.update_checkpoint()

async def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


async def main():
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
    async with client:
        await client.receive_batch(
            on_event_batch=on_event_batch,
            on_error=on_error,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())