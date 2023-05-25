#!/usr/bin/env python3
 
import logging
import json
import time
import grpc
import threading
import traceback

# generated from .proto
import orchestrator_pb2 as orchestrator_pb
import orchestrator_pb2_grpc as orchestrator_pb_grpc

logging.basicConfig(level=logging.DEBUG)

configfile = "config.json"
config = json.load(open(configfile, 'rt'))

log_format = (
    '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')
logger = logging.getLogger("Orchestrator")
logging.basicConfig(level=logging.INFO, format=log_format)


class RequestTaskLoop(threading.Thread):
    def __init__(self, gui_stub, exec_stub, planner_stub):
        threading.Thread.__init__(self)
        self.gui_stub = gui_stub
        self.exec_stub = exec_stub
        self.planner_stub = planner_stub

    def run(self):
        while True:
            try:
                dummy1 = orchestrator_pb.Empty()
                logger.info("Requesting task")
                goal = self.gui_stub.requestTask(dummy1)
                logger.info("Assembling problem")
                problem = self.exec_stub.assembleProblem(goal)
                logger.info("Solving problem")
                solution = self.planner_stub.planOneShot(problem)
                logger.info("Executing plan")
                exec_result = self.exec_stub.processPlanningResult(solution)
                logger.info("Processing plan execution result")
                self.gui_stub.processTaskResult(exec_result)
            except Exception:
                logger.error("exception (retrying after 2 seconds): %s", traceback.format_exc())
                time.sleep(2)
            

       
class GuiSimLoop(threading.Thread):
    def __init__(self, gui_stub, sim_stub):
        threading.Thread.__init__(self)
        self.gui_stub = gui_stub
        self.sim_stub = sim_stub

    def run(self):
        while True:
            try:
                dummy1 = orchestrator_pb.Empty()
                logger.info("Waiting for state to send to simulation...")
                state = self.gui_stub.getState(dummy1)
                logger.info("Setting simulation state")
                self.sim_stub.setState(state)
            except Exception:
                logger.error("exception (retrying after 2 seconds): %s", traceback.format_exc())
                time.sleep(2)
          

class SimStateLoop(threading.Thread):
    def __init__(self, sim_stub, gui_stub, exec_stub):
        threading.Thread.__init__(self)
        self.gui_stub = gui_stub
        self.sim_stub = sim_stub
        self.exec_stub = exec_stub

    def run(self):
        while True:
            try:
                dummy1 = orchestrator_pb.Empty()
                logger.info("Waiting for state to GUI and Executor...")
                state = self.sim_stub.getState(dummy1)
                logger.info("Sending state to executor")
                self.exec_stub.processState(state)
                logger.info("Sending state to GUI")
                self.gui_stub.visualizeState(state)
            except Exception:
                logger.error("exception (retrying after 2 seconds): %s", traceback.format_exc())
                time.sleep(2)
                
            
class DoActionLoop(threading.Thread):
    def __init__(self, sim_stub, exec_stub):
        threading.Thread.__init__(self)
        self.sim_stub = sim_stub
        self.exec_stub = exec_stub

    def run(self):
        while True:
            try:
                dummy1 = orchestrator_pb.Empty()
                logger.info("Waiting for action to execute.")
                action = self.exec_stub.doNextAction(dummy1)
                logger.info("Sending action to simulation.")
                result = self.sim_stub.doAction(action)
                logger.info("Sending action result to executor.")
                self.exec_stub.processActionResult(result)
            except Exception:
                logger.error("exception (retrying after 2 seconds): %s", traceback.format_exc())
                time.sleep(2)            
            

def main():
    guiconn = '0.0.0.0:' + str(config['gui-grpcport'])
    solverconn = '0.0.0.0:' + str(config['solver-grpcport'])
    exec_conn = '0.0.0.0:' + str(config['executor-grpcport'])
    sim_conn = '0.0.0.0:' + str(config['simulation-grpcport'])

    logger.info("connecting to GUI at %s", guiconn)
    gui_channel = grpc.insecure_channel(guiconn)
    gui_stub = orchestrator_pb_grpc.MazeGUIStub(gui_channel)

    logger.info("connecting to Planner at %s", solverconn)
    solver_channel = grpc.insecure_channel(solverconn)
    solver_stub = orchestrator_pb_grpc.UnifiedPlanningStub(solver_channel)

    logger.info("connecting to Executor at %s", exec_conn)
    exec_channel = grpc.insecure_channel(exec_conn)
    exec_stub = orchestrator_pb_grpc.AiddlExecutorStub(exec_channel)

    logger.info("connecting to Simulator at %s", sim_conn)
    sim_channel = grpc.insecure_channel(sim_conn)
    sim_stub = orchestrator_pb_grpc.AiddlSimulatorStub(sim_channel)

    logger.info("starting loops")

    reqTaskLoop = RequestTaskLoop(gui_stub, exec_stub, solver_stub)
    guiSimLoop = GuiSimLoop(gui_stub, sim_stub)
    simStateLoop = SimStateLoop(sim_stub, gui_stub, exec_stub)
    doActionLoop = DoActionLoop(sim_stub, exec_stub)
    
    reqTaskLoop.start()
    guiSimLoop.start()
    simStateLoop.start()
    doActionLoop.start()
    
main()
