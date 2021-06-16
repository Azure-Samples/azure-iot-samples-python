# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
import os
import asyncio
import random
import sys
import signal
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

# The device connection authenticates your device to your IoT hub. The connection string for 
# a device should never be stored in code. For the sake of simplicity we're using an environment 
# variable here. If you created the environment variable with the IDE running, stop and restart 
# the IDE to pick up the environment variable.
#
# You can use the Azure CLI to find the connection string:
#     az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = os.getenv("ConnectionString")
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}}}'

def keyboard_interrupt_handler(signal, frame):
    print ( "IoTHubClient sample stopped" )
    sys.exit(0)

async def main():

    
    print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

    # Process the keyboard interrupt.
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)    

    while True:

        # Build the message with simulated telemetry values.
        temperature = TEMPERATURE + (random.random() * 15)
        humidity = HUMIDITY + (random.random() * 20)
        msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity)
        message = Message(msg_txt_formatted)

        # Add a custom application property to the message.
        # An IoT hub can filter on these properties without access to the message body.
        if temperature > 30:
          message.custom_properties["temperatureAlert"] = "true"
        else:
          message.custom_properties["temperatureAlert"] = "false"

        # Send the message.
        print( "Sending message: {}".format(message) )
        await client.send_message(message)
        print ( "Message successfully sent" )
        await asyncio.sleep(1)

    await client.shutdown()

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    asyncio.run(main())

    # If you are using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
