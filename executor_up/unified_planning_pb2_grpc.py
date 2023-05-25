# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import unified_planning_pb2 as unified__planning__pb2


class UnifiedPlanningStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.planAnytime = channel.unary_stream(
                '/UnifiedPlanning/planAnytime',
                request_serializer=unified__planning__pb2.PlanRequest.SerializeToString,
                response_deserializer=unified__planning__pb2.PlanGenerationResult.FromString,
                )
        self.planOneShot = channel.unary_unary(
                '/UnifiedPlanning/planOneShot',
                request_serializer=unified__planning__pb2.PlanRequest.SerializeToString,
                response_deserializer=unified__planning__pb2.PlanGenerationResult.FromString,
                )
        self.validatePlan = channel.unary_unary(
                '/UnifiedPlanning/validatePlan',
                request_serializer=unified__planning__pb2.ValidationRequest.SerializeToString,
                response_deserializer=unified__planning__pb2.ValidationResult.FromString,
                )
        self.compile = channel.unary_unary(
                '/UnifiedPlanning/compile',
                request_serializer=unified__planning__pb2.Problem.SerializeToString,
                response_deserializer=unified__planning__pb2.CompilerResult.FromString,
                )


class UnifiedPlanningServicer(object):
    """Missing associated documentation comment in .proto file."""

    def planAnytime(self, request, context):
        """An anytime plan request to the engine.
        The engine replies with a stream of N `Answer` messages where:
        - the first (N-1) message are of type `IntermediateReport`
        - the last message is of type `FinalReport`
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def planOneShot(self, request, context):
        """A oneshot plan request to the engine.
        The engine replies with athe PlanGenerationResult
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def validatePlan(self, request, context):
        """A validation request to the engine.
        The engine replies with the ValidationResult
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def compile(self, request, context):
        """A compiler request to the engine.
        The engine replies with the CompilerResult
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UnifiedPlanningServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'planAnytime': grpc.unary_stream_rpc_method_handler(
                    servicer.planAnytime,
                    request_deserializer=unified__planning__pb2.PlanRequest.FromString,
                    response_serializer=unified__planning__pb2.PlanGenerationResult.SerializeToString,
            ),
            'planOneShot': grpc.unary_unary_rpc_method_handler(
                    servicer.planOneShot,
                    request_deserializer=unified__planning__pb2.PlanRequest.FromString,
                    response_serializer=unified__planning__pb2.PlanGenerationResult.SerializeToString,
            ),
            'validatePlan': grpc.unary_unary_rpc_method_handler(
                    servicer.validatePlan,
                    request_deserializer=unified__planning__pb2.ValidationRequest.FromString,
                    response_serializer=unified__planning__pb2.ValidationResult.SerializeToString,
            ),
            'compile': grpc.unary_unary_rpc_method_handler(
                    servicer.compile,
                    request_deserializer=unified__planning__pb2.Problem.FromString,
                    response_serializer=unified__planning__pb2.CompilerResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'UnifiedPlanning', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UnifiedPlanning(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def planAnytime(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/UnifiedPlanning/planAnytime',
            unified__planning__pb2.PlanRequest.SerializeToString,
            unified__planning__pb2.PlanGenerationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def planOneShot(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UnifiedPlanning/planOneShot',
            unified__planning__pb2.PlanRequest.SerializeToString,
            unified__planning__pb2.PlanGenerationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def validatePlan(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UnifiedPlanning/validatePlan',
            unified__planning__pb2.ValidationRequest.SerializeToString,
            unified__planning__pb2.ValidationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def compile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UnifiedPlanning/compile',
            unified__planning__pb2.Problem.SerializeToString,
            unified__planning__pb2.CompilerResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
