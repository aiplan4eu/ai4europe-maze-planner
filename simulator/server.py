from concurrent import futures

import logging
import time
import grpc

import simulator_pb2 as simulator_pb2
import simulator_pb2_grpc as simulator_pb2_grpc

from aiddl_core.representation import Sym
from aiddl_core.representation import Tuple
from aiddl_core.representation import KeyVal
from aiddl_core.representation import Set
from aiddl_core.parser.parser import parse_term

log_format = (
    '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')
logger = logging.getLogger("AIDDL Simulator")
logging.basicConfig(level=logging.INFO, format=log_format)


class SimulationServicer(simulator_pb2_grpc.AiddlSimulatorServicer):
    SUCCESS = Sym("success")
    FAILURE = Sym("failure")
    
    def __init__(self, operators, port):
        self.port = port
        self.state = Set([])
        self.operators = operators
        self.state_updated = False
        
    def doAction(self, request, context):
        action = parse_term(request.action)
        logging.info("received action: %s" % action)

        op = None
        for o in self.operators:
            s = o[Sym("name")].match(action)
            if s is not None:
                applicable = True
                o_sub = o.substitute(s)
                logger.info("Found matching operator: %s\ntesting applicability..." % str(o_sub))
                for p in o_sub[Sym("preconditions")]:
                    if self.state[p.key] is None \
                       or self.state[p.key] != p.value:
                        applicable = Falseo
                        break
                if applicable:
                    logger.info("Operator applicable.")
                    op = o_sub
                    break
                else:
                    logger.info("Operator not applicable.")

        time.sleep(0.5)
        if op is None:
            logger.info("action cannot be applied.")
            self.state_updated = True
            logger.info("sending failure message") 
            return simulator_pb2.Result(result=str(SimulationServicer.FAILURE))            
        else:
            logger.info("applicable operator: %s" % str(op))
            self.state = self.state.put_all(op[Sym("effects")])
            self.state_updated = True
            logger.info("waiting for state update to be sent") 
            while self.state_updated:
                time.sleep(0.2)
            logger.info("sending success message") 
            return simulator_pb2.Result(result=str(SimulationServicer.SUCCESS))

    def getState(self, request, context):
        while not self.state_updated:
            time.sleep(0.1)
        logger.info("sending state update.")
        self.state_updated = False
        return simulator_pb2.State(state=str(self.state))

    def setState(self, request, context):
        self.state = parse_term(request.state)
        logger.info("Received state override.")
        self.state_updated = True
        return simulator_pb2.Empty()
    
    def start(self):
        connection = '0.0.0.0:%d' % (self.port)
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        simulator_pb2_grpc.add_AiddlSimulatorServicer_to_server(
            self, self.server)
        self.server.add_insecure_port(connection)
        self.server.start()
        logger.info("server started on %s" % connection)

    def wait_for_termination(self):
        self.server.wait_for_termination()
