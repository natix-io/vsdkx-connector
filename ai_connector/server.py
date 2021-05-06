from concurrent import futures

from ai_connector.client import connect_module_pb2
from ai_connector.client import connect_module_pb2_grpc
import grpc
import os
from ai_connector.utils.serialisation import unpickle_frame_from_message
from ai_connector.utils.serialisation import serialize_inference_result
from ai_connector.utils.yaml_utils import parse_yaml_string_to_dict

DEFAULT_PORT = 7914


class Server:
    """
    This is a class with all the functions related to the gRPC server
    launch, execution, etc
    """

    @staticmethod
    def run(event_detector_interface, port: str = None):
        """
        Function to start gRPC server, pass service class to it, add dedicated
        port to operate through and wait for termination
        Args:
            event_detector_interface: this is a class that should have the
                predict method which accepts image.
            port: This is the gRPC server port, if it is None, it would be
                retrieved from environment (GRPC_PORT)
        """
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        module = ConnectVisionX(event_detector_interface)

        connect_module_pb2_grpc.add_ConnectModuleServicer_to_server(module,
                                                                    server)
        grpc_port = port if port is not None else os.getenv("GRPC_PORT"
                                                            , DEFAULT_PORT)
        server.add_insecure_port(f'[::]:{grpc_port}')
        server.start()
        print(f"gRPC server is running on port {grpc_port}")
        server.wait_for_termination()


class ConnectVisionX(connect_module_pb2_grpc.ConnectModuleServicer):
    """
    gRPC Service class, inheriting from a parent defined in gRPC client code,
    with remote procedure methods implemented and ready to be executed when
    called by gRPC.

    Attributes:
        event_detector_interface: This interface should have
            the predict(img) function for prediction
    """

    def __init__(self, event_detector_interface):
        """
        event_detector_interface: this is a class that should have the predict
            method which accepts image.
        """
        self.event_detector_interface = event_detector_interface
        self.event_detector_instance = None


    def Configure(self, request, context):
        """
        configuration passed as yaml string

        Args:
            request (Configuration object): gRPC message containing
            configuration byte string in yaml format
            context (Context object): low level gRPC data about request details

        Returns:
            (StatusCode object): gRPC message object containing status variable
            with value of 1 if configuration process is successful or 0 if
            error has occurred
        """
        # Try parsing received yaml string into dictionary of configuration
        # If everything goes fine, set status code to 1
        # Except in case of something going wrong, log the exception and set
        # status code to be returned to 0
        try:
            config = request.conf
            config_dict = parse_yaml_string_to_dict(config)
            system_config = config_dict.get("system_config")
            base_path = config_dict.get("base_path")
            self.event_detector_instance = self.event_detector_interface(
                system_config=system_config,
                base_path=base_path
            )
            response = connect_module_pb2.StatusCode(status=1)
        except Exception as e:
            print(f"Configure procedure call raised Error: {e}, {type(e)}")
            response = connect_module_pb2.StatusCode(status=0)

        return response

    def ProcessFrame(self, request_iterator, context):
        """
        Remote procedure receives byte string chunks in serialized form,
        unpacks them, concatenates and deserializes into frame.
        Calls predict method on received frame and config_dict.

        Args:
            request_iterator (Generator object): gRPC messages containing
            byte string chunks of a serialized frame
            context (Context object): low level gRPC data about
            request details

        Returns:
            (Inference object): serialized tuple of inference results returned
            from predict_method
        """
        frame_bytes = b''.join(
            request.frame_chunk for request in request_iterator
        )

        frame = unpickle_frame_from_message(frame_bytes)
        inference = self.event_detector_instance.predict(frame)

        response = connect_module_pb2.Inference()
        response.result = serialize_inference_result(inference)

        return response
