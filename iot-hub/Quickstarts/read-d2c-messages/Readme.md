# Read device to cloud messages (Python)

Use the Microsoft Azure Event Hubs Client for Python to read messages sent from a device by using the
built-in event hubs that exists by default for every Iot Hub instance. For more details, see the 
documentation for the [azure-eventhub](https://pypi.org/project/azure-eventhub/) package.

## Get Event Hubs-compatible connection string

You can get the Event Hubs-compatible connection string to your IotHub instance via the Azure portal or
by using the Azure CLI.

If using the Azure portal, see [Built in endpoints for IotHub](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-read-builtin#read-from-the-built-in-endpoint) to get the Event Hubs-compatible
connection string.

If using the Azure CLI, you will need to run the below to get the Event Hubs-compatible endpoint, path
and the SAS key for the "service" policy.

- `az iot hub show --query properties.eventHubEndpoints.events.endpoint --name {your IoT Hub name}`
- `az iot hub show --query properties.eventHubEndpoints.events.path --name {your IoT Hub name}`
- `az iot hub policy show --name service --query primaryKey --hub-name {your IoT Hub name}`

Then, form the Event Hubs-compatible connection string as below
`Endpoint=eventHubsCompatibleEndpoint/;EntityPath=eventHubsCompatiblePath;SharedAccessKeyName=service;SharedAccessKey=iotHubSasKey`.

With the Event Hubs-compatible connection string now in hand, you can now use the EventHubConsumerClient from the
[azure-eventhub](https://pypi.org/project/azure-eventhub/) package as shown in any of the receive related samples below
- [sync samples](https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/eventhub/azure-eventhub/samples/sync_samples)
- [async samples](https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/eventhub/azure-eventhub/samples/async_samples)

If you cannot get the Event Hubs-compatible connection string in the above manner, and need to programatically get this information,
then use the [sample to convert IotHub connection string to an Event Hubs-compatible one](https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/eventhub/azure-eventhub/samples/async_samples/iot_hub_connection_string_receive_async.py). This conversion is done by connecting to 
the IoT hub endpoint and receiving a redirection address to the built-in event hubs. This address is then used 
in the Event Hubs Client to read messages.

## Checkpointing

For an example that uses checkpointing, use the checkpoint store from
- [azure-eventhub-checkpointstoreblob](https://pypi.org/project/azure-eventhub-checkpointstoreblob/) package for sync
- [azure-eventhub-checkpointstoreblob-aio](https://pypi.org/project/azure-eventhub-checkpointstoreblob-aio/) package for async

The above links have documentation on samples on how to use the checkpoint store.




