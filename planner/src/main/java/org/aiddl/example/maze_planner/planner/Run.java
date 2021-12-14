package org.aiddl.example.maze_planner.planner;

import java.io.IOException;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

import org.aiddl.common.java.CommonTerm;
import org.aiddl.common.java.planning.state_variable.ForwardSearchPlanIterator;
import org.aiddl.core.java.parser.Parser;
import org.aiddl.core.java.representation.Term;
import org.aiddl.core.java.tools.Profiler;
import org.aiddl.core.java.tools.StopWatch;
import org.aiddl.example.maze_planner.planner.AiddlPlannerGrpc.AiddlPlannerImplBase;
import org.aiddl.example.maze_planner.planner.Planner.Problem;
import org.aiddl.example.maze_planner.planner.Planner.Solution;
import org.aiddl.example.maze_planner.planner.Planner.Solution.Builder;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;

public class Run {
	
	private static final Logger logger =   Logger.getLogger(Run.class.getName());

	  private final int port;
	  private final Server server;

	  public Run(int port) throws IOException {
		  this.port = port;
		  server = ServerBuilder.forPort(port).addService(new PlannerService())
				  .build();
	  }

	  /** Start serving requests. */
	  public void start() throws IOException {
	    server.start();
	    logger.info("Server started, listening on " + port);
	    Runtime.getRuntime().addShutdownHook(new Thread() {
	      @Override
	      public void run() {
	        // Use stderr here since the logger may have been reset by its JVM shutdown hook.
	        System.err.println("*** shutting down gRPC server since JVM is shutting down");
	        try {
	        	Run.this.stop();
	        } catch (InterruptedException e) {
	          e.printStackTrace(System.err);
	        }
	        System.err.println("*** server shut down");
	      }
	    });
	  }

	  /** Stop serving requests and shutdown resources. */
	  public void stop() throws InterruptedException {
	    if (server != null) {
	      server.shutdown().awaitTermination(30, TimeUnit.SECONDS);
	    }
	  }

	  /**
	   * Await termination on the main thread since the grpc library uses daemon threads.
	   */
	  private void blockUntilShutdown() throws InterruptedException {
	    if (server != null) {
	      server.awaitTermination();
	    }
	  }

	
	public static void main( String[] args ) throws IOException, InterruptedException {
	    Run server = new Run(8061);
	    server.start();
	    server.blockUntilShutdown();
	}
	
	private static class PlannerService extends AiddlPlannerImplBase {

		public PlannerService() {
	      
	    }

	    @Override
	    public void plan(Problem request, StreamObserver<Solution> responseObserver) {
	      responseObserver.onNext(runPlanner(request));
	      responseObserver.onCompleted();
	    }
	    
	    private Solution runPlanner(Problem problem) {
			System.out.println("Protobuf Problem object:");
			System.out.println("========================================");
			System.out.println(problem);
			System.out.println("========================================");
	    	
			Term problemTerm = Parser.ParseTerm(problem.getProblem());
		
			ForwardSearchPlanIterator planner = new ForwardSearchPlanIterator();
			planner.initialize(problemTerm);
			Term pi = planner.apply(Term.sym("next"));
				
			Builder s; 
			if ( pi.equals(CommonTerm.NIL) ) {
				s = Solution.newBuilder().setStatus(1);
				System.out.println("No plan found.");
			} else {
				s = Solution.newBuilder().setStatus(0);
				int idx = 0;
				System.out.println("Plan:");
				for ( Term a : pi.asList() ) {
					System.out.println("\t" + a);
					s.addAction(pi.get(idx).toString());
					idx++;
				}
			}
			Solution s_built = s.build();
			System.out.println("Protobuf Solution object:");
			System.out.println("========================================");
			System.out.println(s_built);
			System.out.println("========================================");
			System.out.println(StopWatch.allSums2Str());
			System.out.println(Profiler.getString());
			return s_built;
	    }
	}	
}
