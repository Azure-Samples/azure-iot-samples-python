# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

# For guidance, see https://docs.microsoft.com/azure/iot-edge/tutorial-python-module

import sys
import threading
import signal
from azure.iot.device import IoTHubModuleClient

# global counters
RECEIVED_MESSAGES = 0

def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    # define function for handling received messages
    def receive_message_handler(message):
        # NOTE: This function only handles messages sent to "input1".
        # Messages sent to other inputs or to the default will be discarded.
        global RECEIVED_MESSAGES
        if message.input_name == "input1":
            RECEIVED_MESSAGES += 1
            print("Message received on input1")
            print( "    Data: <<{}>>".format(message.data) )
            print( "    Properties: {}".format(message.custom_properties))
            print( "    Total calls received: {}".format(RECEIVED_MESSAGES))
            print("Forwarding message to output1")
            client.send_message_to_output(message, "output1")
            print("Message successfully forwarded")
        else:
            print("Message received on unknown input: {}".format(message.input_name))

    # Set handler
    client.on_message_received = receive_message_handler

    return client


def main():
    print ( "\nPython {}\n".format(sys.version) )
    print ( "IoT Hub Client for Python" )

    client = create_client()

    # Event indicating client stop
    stop_event = threading.Event()

    # Define a signal handler that will indicate Edge termination of the Module
    def module_termination_handler(signal, frame):
        print ("IoTHubClient sample stopped")
        stop_event.set()

    # Attach the signal handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    try:
        # This will be triggered by Edge termination signal
        stop_event.wait()
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        # Graceful exit
        print("Shutting down client")
        client.shutdown()

if __name__ == '__main__':
    main()
