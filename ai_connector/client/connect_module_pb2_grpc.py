# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import connect_module_pb2 as connect__module__pb2


class ConnectModuleStub(object):
    """Define gRPC service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ProcessFrame = channel.stream_unary(
                '/ConnectModule/ProcessFrame',
                request_serializer=connect__module__pb2.FrameRequest.SerializeToString,
                response_deserializer=connect__module__pb2.Inference.FromString,
                )
        self.Configure = channel.unary_unary(
                '/ConnectModule/Configure',
                request_serializer=connect__module__pb2.Configuration.SerializeToString,
                response_deserializer=connect__module__pb2.StatusCode.FromString,
                )


class ConnectModuleServicer(object):
    """Define gRPC service
    """

    def ProcessFrame(self, request_iterator, context):
        """Send frame and retrieve inference
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Configure(self, request, context):
        """Send Configuration and retrieve status code
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ConnectModuleServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ProcessFrame': grpc.stream_unary_rpc_method_handler(
                    servicer.ProcessFrame,
                    request_deserializer=connect__module__pb2.FrameRequest.FromString,
                    response_serializer=connect__module__pb2.Inference.SerializeToString,
            ),
            'Configure': grpc.unary_unary_rpc_method_handler(
                    servicer.Configure,
                    request_deserializer=connect__module__pb2.Configuration.FromString,
                    response_serializer=connect__module__pb2.StatusCode.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ConnectModule', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ConnectModule(object):
    """Define gRPC service
    """

    @staticmethod
    def ProcessFrame(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/ConnectModule/ProcessFrame',
            connect__module__pb2.FrameRequest.SerializeToString,
            connect__module__pb2.Inference.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Configure(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ConnectModule/Configure',
            connect__module__pb2.Configuration.SerializeToString,
            connect__module__pb2.StatusCode.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)