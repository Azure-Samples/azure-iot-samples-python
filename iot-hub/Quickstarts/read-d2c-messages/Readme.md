# Read device to cloud messages (Python)

Currently there is no pip available for the Azure Event Hubs client.

The options are:

* Build a docker image.
* Build the libraries manually.

For more information, see https://github.com/Azure/azure-event-hubs-python

To keep this quickstart simple, you are using the iothub-explorer CLI tool to monitor telemetry sent to the hub:

npm install -g iothub-explorer
iothub-explorer monitor-events MyPythonDevice --login {your hub service connection string}