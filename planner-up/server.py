from concurrent import futures

import logging
import time
import grpc

from unified_planning.engines.results import POSITIVE_OUTCOMES
from unified_planning.shortcuts import Problem, OneshotPlanner
from unified_planning.io import PythonWriter
from unified_planning.io import PDDLWriter

import planner_pb2 as planner_pb2
import planner_pb2_grpc as planner_pb2_grpc

from aiddl_core.representation.sym import Sym
from aiddl_core.representation.tuple import Tuple
from aiddl_core.representation.key_value import KeyValue
from aiddl_core.representation.set import Set
from aiddl_core.parser.parser import parse_term
from aiddl_core.tools.logger import Logger

from converter import aiddl_svp_2_up

log_format = (
    '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')
logger = logging.getLogger("AIDDL Unified Planning Bridge")
logging.basicConfig(level=logging.INFO, format=log_format)


class UnifiedPlanningServicer(planner_pb2_grpc.AiddlPlannerServicer):
    def __init__(self, port):
        self.port = port

    def plan(self, request, context):
        logger.info("assembling problem")
        problem = parse_term(request.problem)

        logger.info(Logger.pretty_print(problem, 1))

        logger.info("Converting AIDDL 2 UP problem...")
        problem_up = aiddl_svp_2_up(problem, "maze")

        # writer = PythonWriter(problem_up)
        writer = PDDLWriter(problem_up)

        logger.info("UP Domain:")
        logger.info(writer.get_domain())

        logger.info("UP Problem:")
        logger.info(writer.get_problem())
        
        response = planner_pb2.Solution(status=1, action=[])

        logger.info("Problem kind: %s" % (problem_up.kind))

        with OneshotPlanner(problem_kind=problem_up.kind) as planner:
            logger.info("Running UP...")
            final_report = planner.solve(problem_up)
            logger.info("Assembling response from report...")

            logger.info(str(final_report))
            
            if final_report.status in POSITIVE_OUTCOMES:
                plan = final_report.plan

                actions = []
                for a in plan.actions:
                    a_list = []
                    a_list.append(Sym(a.action.name))
                    for p in a.actual_parameters:
                        a_list.append(Sym(str(p)))
                    aiddl_action = Tuple(a_list)
                    actions.append(str(aiddl_action))
                
                response = planner_pb2.Solution(status=0, action=actions)

        
        
        return response
    
    def start(self):
        connection = '0.0.0.0:%d' % (self.port)
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        planner_pb2_grpc.add_AiddlPlannerServicer_to_server(
            self, self.server)
        self.server.add_insecure_port(connection)
        self.server.start()
        logger.info("server started on %s" % connection)
        
    def wait_for_termination(self):
        self.server.wait_for_termination()
