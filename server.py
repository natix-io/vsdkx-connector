from concurrent import futures

import client.connect_module_pb2 as connect_module_pb2
import client.connect_module_pb2_grpc as connect_module_pb2_grpc
import grpc
import os
from utils.serialisation import unpickle_frame_from_message
from utils.serialisation import serialize_inference_result
from utils.yaml_utils import parse_yaml_string_to_dict

DEFAULT_PORT = 7914


class Server:
    """
    This is a class with all the functions related to the gRPC server
    launch, execution, etc
    """

    @staticmethod
    def run(predict_method, port: str = None):
        """
        Function to start gRPC server, pass service class to it, add dedicated
        port to operate through and wait for termination
        Args:
            predict_method: this is a method that we pass image and config_dict to that.
            port: This is the gRPC server port, if it is None, it would be retrieved from environment (GRPC_PORT)
        """
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        module = ConnectVisionX(port if port is not None else os.getenv("GRPC_PORT", DEFAULT_PORT), predict_method)

        connect_module_pb2_grpc.add_ConnectModuleServicer_to_server(module,
                                                                    server)
        server.add_insecure_port(f'[::]:{module.port}')
        server.start()
        print(f"gRPC server is running on port {module.port}")
        server.wait_for_termination()


class ConnectVisionX(connect_module_pb2_grpc.ConnectModuleServicer):
    """
    gRPC Service class, inheriting from a parent defined in gRPC client code,
    with remote procedure methods implemented and ready to be executed when
    called by gRPC.

    Attributes:
        port (str): port number retrieved during server run
        predict_method (predict method of AI Processor): we pass the image and config dict to this method
        for prediction
    """

    def __init__(self, port, predict_method):
        """
        Set port number which would be retrieved during server run.
        Create and store instance of EventDetector class
        """
        self.port = port
        self.predict_method = predict_method
        self.config_dict = None

    def Configure(self, request, context):
        """
        Remote procedure to create new instance of EventDetector class with
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
        # settings and initialize and store new instance of EventDetector into
        # event_detector attribute, with received configuration.
        # If everything goes fine, set status code to 1
        # Except in case of something going wrong, log the exception and set
        # status code to be returned to 0
        try:
            config = request.conf
            self.config_dict = parse_yaml_string_to_dict(config)
            response = connect_module_pb2.StatusCode(status=1)
        except Exception as e:
            print(f"Configure procedure call raised Error: {e}, {type(e)}")
            response = connect_module_pb2.StatusCode(status=0)

        return response

    def ProcessFrame(self, request_iterator, context):
        """
        Remote procedure receives byte string chunks in serialized form,
        unpacks them, concatenates and deserializes into frame.
        Calls predict method of EventDetector on received frame.

        Args:
            request_iterator (Generator object): gRPC messages containing
            byte string chunks of a serialized frame
            context (Context object): low level gRPC data about
            request details

        Returns:
            (Inference object): serialized tuple of inference results returned
            from EventDetector prediction
        """
        frame_bytes = b''
        for request in request_iterator:
            frame_bytes += request.frame_chunk

        frame = unpickle_frame_from_message(frame_bytes)
        inference = self.predict_method(frame, self.config_dict)

        response = connect_module_pb2.Inference()
        response.result = serialize_inference_result(inference)

        return response
