# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import executor_pb2 as executor__pb2
import unified_planning_pb2 as unified__planning__pb2


class AiddlExecutorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.assembleProblem = channel.unary_unary(
                '/AiddlExecutor/assembleProblem',
                request_serializer=executor__pb2.AiddlGoal.SerializeToString,
                response_deserializer=unified__planning__pb2.PlanRequest.FromString,
                )
        self.doNextAction = channel.unary_unary(
                '/AiddlExecutor/doNextAction',
                request_serializer=executor__pb2.Empty.SerializeToString,
                response_deserializer=executor__pb2.AiddlAction.FromString,
                )
        self.processPlanningResult = channel.unary_unary(
                '/AiddlExecutor/processPlanningResult',
                request_serializer=unified__planning__pb2.PlanGenerationResult.SerializeToString,
                response_deserializer=executor__pb2.AiddlResult.FromString,
                )
        self.processActionResult = channel.unary_unary(
                '/AiddlExecutor/processActionResult',
                request_serializer=executor__pb2.AiddlResult.SerializeToString,
                response_deserializer=executor__pb2.Empty.FromString,
                )
        self.processState = channel.unary_unary(
                '/AiddlExecutor/processState',
                request_serializer=executor__pb2.AiddlState.SerializeToString,
                response_deserializer=executor__pb2.Empty.FromString,
                )
        self.setOperators = channel.unary_unary(
                '/AiddlExecutor/setOperators',
                request_serializer=executor__pb2.AiddlOperators.SerializeToString,
                response_deserializer=executor__pb2.Empty.FromString,
                )


class AiddlExecutorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def assembleProblem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def doNextAction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def processPlanningResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def processActionResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def processState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setOperators(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AiddlExecutorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'assembleProblem': grpc.unary_unary_rpc_method_handler(
                    servicer.assembleProblem,
                    request_deserializer=executor__pb2.AiddlGoal.FromString,
                    response_serializer=unified__planning__pb2.PlanRequest.SerializeToString,
            ),
            'doNextAction': grpc.unary_unary_rpc_method_handler(
                    servicer.doNextAction,
                    request_deserializer=executor__pb2.Empty.FromString,
                    response_serializer=executor__pb2.AiddlAction.SerializeToString,
            ),
            'processPlanningResult': grpc.unary_unary_rpc_method_handler(
                    servicer.processPlanningResult,
                    request_deserializer=unified__planning__pb2.PlanGenerationResult.FromString,
                    response_serializer=executor__pb2.AiddlResult.SerializeToString,
            ),
            'processActionResult': grpc.unary_unary_rpc_method_handler(
                    servicer.processActionResult,
                    request_deserializer=executor__pb2.AiddlResult.FromString,
                    response_serializer=executor__pb2.Empty.SerializeToString,
            ),
            'processState': grpc.unary_unary_rpc_method_handler(
                    servicer.processState,
                    request_deserializer=executor__pb2.AiddlState.FromString,
                    response_serializer=executor__pb2.Empty.SerializeToString,
            ),
            'setOperators': grpc.unary_unary_rpc_method_handler(
                    servicer.setOperators,
                    request_deserializer=executor__pb2.AiddlOperators.FromString,
                    response_serializer=executor__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AiddlExecutor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AiddlExecutor(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def assembleProblem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AiddlExecutor/assembleProblem',
            executor__pb2.AiddlGoal.SerializeToString,
            unified__planning__pb2.PlanRequest.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def doNextAction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AiddlExecutor/doNextAction',
            executor__pb2.Empty.SerializeToString,
            executor__pb2.AiddlAction.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def processPlanningResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AiddlExecutor/processPlanningResult',
            unified__planning__pb2.PlanGenerationResult.SerializeToString,
            executor__pb2.AiddlResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def processActionResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AiddlExecutor/processActionResult',
            executor__pb2.AiddlResult.SerializeToString,
            executor__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def processState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AiddlExecutor/processState',
            executor__pb2.AiddlState.SerializeToString,
            executor__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def setOperators(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AiddlExecutor/setOperators',
            executor__pb2.AiddlOperators.SerializeToString,
            executor__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
