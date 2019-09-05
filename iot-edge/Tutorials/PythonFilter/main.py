# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

# For guidance, see https://docs.microsoft.com/azure/iot-edge/tutorial-python-module

import sys
import time
import threading
from azure.iot.device import IoTHubModuleClient, Message

# global counters
RECEIVED_MESSAGES = 0

def receive_message_listener(client):
    # This listener function only triggers for messages sent to "input1".
    # Messages sent to other inputs or to the default will be silently discarded.
    global RECEIVED_MESSAGES
    while True:
        message = client.receive_message_on_input("input1")   # blocking call
        RECEIVED_MESSAGES += 1
        print("Message received on input1")
        print( "    Data: <<{}>>".format(message.data) )
        print( "    Properties: {}".format(message.custom_properties))
        print( "    Total calls received: {}".format(RECEIVED_MESSAGES))
        print("Forwarding message to output1")
        client.send_message_to_output(message, "output1")
        print("Message successfully forwarded")

def main():
    try:
        print ( "\nPython {}\n".format(sys.version) )
        print ( "IoT Hub Client for Python" )

        client = IoTHubModuleClient.create_from_edge_environment()

        # Begin listening for messages
        message_listener_thread = threading.Thread(target=receive_message_listener, args=(client,))
        message_listener_thread.daemon = True
        message_listener_thread.start()

        print ( "Starting the IoT Hub Python sample...")
        print ( "The sample is now waiting for messages and will indefinitely.  Press Ctrl-C to exit. ")

        while True:
            time.sleep(1000)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
    except:
        print ( "Unexpected error from IoTHub" )
        return

if __name__ == '__main__':
    try:
        main()

    except Exception as error:
        print ( error )
        sys.exit(1)
