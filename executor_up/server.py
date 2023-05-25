from concurrent import futures

import logging
import time
import grpc

import executor_pb2 as executor_pb2
import executor_pb2_grpc as executor_pb2_grpc
import unified_planning.grpc.generated.unified_planning_pb2 as up_pb2
import unified_planning.grpc.generated.unified_planning_pb2_grpc as up_pb2_grpc

from aiddl_core.representation import Sym
from aiddl_core.representation import Tuple
from aiddl_core.representation import KeyVal
from aiddl_core.representation import Set
from aiddl_core.parser.parser import parse_term

from unified_planning.grpc.proto_writer import ProtobufWriter

from convert_to_up import aiddl_svp_2_up
from convert_to_up import up_action_2_aiddl

log_format = (
    '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')
logger = logging.getLogger("AIDDL Executor")
logging.basicConfig(level=logging.INFO, format=log_format)


class ExecutionServicer(executor_pb2_grpc.AiddlExecutorServicer):
    SUCCESS = Sym("success")
    FAILURE = Sym("failure")
    
    def __init__(self, port, operators, domains, signatures):
        self.port = port

        self.state = Set([])
        self.goal = Set([])
        self.operators = operators
        self.domains = domains
        self.signatures = signatures

        self.plan_exec_result = ExecutionServicer.SUCCESS
        self.action_result = ExecutionServicer.SUCCESS
        self.scheduled_actions = []

    def assembleProblem(self, request, context):
        logger.info("assembling problem")
        self.goal = parse_term(request.goal)
        problem = Tuple([
            KeyVal(Sym("domains"), self.domains),
            KeyVal(Sym("signatures"), self.signatures),
            KeyVal(Sym("initial-state"), self.state),
            KeyVal(Sym("goal"), self.goal),
            KeyVal(Sym("operators"), self.operators)
        ])

        writer = ProtobufWriter()
        up_problem = aiddl_svp_2_up(problem, "maze-problem")
        pb_problem = writer.convert(up_problem)
        
        request = up_pb2.PlanRequest(
            problem=pb_problem,
            resolution_mode=up_pb2.PlanRequest.SATISFIABLE,
        )
        
        return request

    def doNextAction(self, request, context):
        logger.info("waiting for previous action to finish or plan to be set")
        while self.action_result is None or self.scheduled_actions == []:
            time.sleep(0.1)
        logger.info("do next action")
        action = self.scheduled_actions[0]
        del self.scheduled_actions[0]
        self.action_result = None
        return executor_pb2.AiddlAction(action=str(action))

    def processPlanningResult(self, request, context):
        logger.info("processing planning result")
        if request.status == up_pb2.PlanGenerationResult.Status.UNSOLVABLE_PROVEN:
            return executor_pb2.AiddlResult(result="NO-PLAN-FOUND")
        else:
            self.scheduled_actions = [up_action_2_aiddl(a) for a in request.plan.actions]
            self.action_result = ExecutionServicer.SUCCESS
            self.plan_exec_result = None

            logger.info("waiting for plan execution to finish")
            while self.plan_exec_result is None and self.scheduled_actions != []:
                time.sleep(0.1)
            
            return executor_pb2.AiddlResult(result=str(self.plan_exec_result))            

            

    def processActionResult(self, request, context):
        action_result = parse_term(request.result)
        logger.info("processing action result: %s" % str(action_result))                

        if action_result != ExecutionServicer.SUCCESS:
            logger.info("failure")
            self.plan_exec_result = ExecutionServicer.FAILURE
            self.scheduled_actions = []
        self.action_result = action_result
        return executor_pb2.Empty()

    def processState(self, request, context):
        logger.info("processing state")
        self.state = parse_term(request.state)
        return executor_pb2.Empty()
    
    def start(self):
        connection = '0.0.0.0:%d' % (self.port)
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        executor_pb2_grpc.add_AiddlExecutorServicer_to_server(
            self, self.server)
        self.server.add_insecure_port(connection)
        self.server.start()
        logger.info("server started on %s" % connection)
        
    def wait_for_termination(self):
        self.server.wait_for_termination()
