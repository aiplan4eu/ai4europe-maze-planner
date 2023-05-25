import time
import logging
import grpc

from concurrent import futures

from aiddl_core.representation import Sym
from aiddl_core.representation import Int
from aiddl_core.representation import Tuple
from aiddl_core.parser.parser import parse_term

import gui_pb2 as gui_pb2
import gui_pb2_grpc as gui_pb2_grpc

log_format = (
    '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')
logger = logging.getLogger("Maze GUI")
logging.basicConfig(level=logging.INFO, format=log_format)


class GuiServicer(gui_pb2_grpc.MazeGUIServicer):
    """Provide problem on request."""

    def __init__(self, port, gui):
        self.port = port
        self.gui = gui
        self.problem = None

        self.gui.add_task_request_callback(self.set_goal)
        self.gui.add_send_state_callback(self.set_state)

        self.goal = None
        self.state = None

    def set_goal(self, goal):
        self.goal = goal

    def set_state(self, state):
        self.state = state

    def requestTask(self, request, context):
        '''Assemble problem from GUI data and submit.'''
        while self.goal is None:
            time.sleep(0.1)
        logger.info("sending task:", self.goal)
        result = gui_pb2.Goal(goal=str(self.goal))
        self.goal = None
        return result

    def processTaskResult(self, request, context):
        '''Assemble problem from GUI data and submit'''
        logger.info("received result:", request.result)
        self.gui.display_result(parse_term(request.result))
        return gui_pb2.Empty()

    def visualizeState(self, request, context):
        '''Display a state.'''
        logger.info("received state to display:", request.state)
        self.gui.display_state(parse_term(request.state))
        return gui_pb2.Empty()

    def getState(self, request, context):
        '''Send assembled state.'''
        while self.state is None:
            time.sleep(0.1)
        state_str = str(self.state)
        logger.info("sending state:", state_str)
        self.state = None
        return gui_pb2.State(state=state_str)
                                
    def start(self):
        connection = '0.0.0.0:%d' % (self.port)
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        gui_pb2_grpc.add_MazeGUIServicer_to_server(self, self.server)
        self.server.add_insecure_port(connection)
        self.server.start()
        logger.info("server started on %s" % connection)

    def wait_for_termination(self):
        self.server.wait_for_termination()
