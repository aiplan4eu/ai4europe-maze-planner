package org.aiddl.example.maze_planner.planner;

import org.aiddl.common.java.CommonTerm;
import org.aiddl.common.java.planning.PlanningTerm;
import org.aiddl.core.java.container.Container;
import org.aiddl.core.java.container.Entry;
import org.aiddl.core.java.function.DefaultFunctions;
import org.aiddl.core.java.function.FunctionRegistry;
import org.aiddl.core.java.parser.Parser;
import org.aiddl.core.java.representation.Term;
import org.aiddl.util.java.request.RequestHandler;
import org.aiddl.core.java.tools.Profiler;
import org.aiddl.core.java.tools.StopWatch;

public class RunOffline {

	public static void main(String[] args) {
		Container db = new Container();
		FunctionRegistry fReg = DefaultFunctions.createDefaultRegistry(db);
		
		Term data_module = Parser.parseFile("../aiddl/maze-dump.aiddl", db, fReg);
		Term planner_module = Term.sym("org.aiddl.common.planning.state-variable.solver.forward-search"); 
		
		Parser.parseFile(Parser.getModuleFilename(planner_module), db, fReg);
		Term exec_module = Term.sym("org.aiddl.examples.run-module");		
		db.addModule(exec_module);
			
		RequestHandler server = new RequestHandler( fReg );
		
		Term Pi = db.getEntry(data_module, Term.sym("problem")).getValue();
		Term s0 = Pi.get(PlanningTerm.InitialState);
		Term g = Pi.get(PlanningTerm.Goal);
		Term O = Pi.get(PlanningTerm.Operators);
		
//		System.out.println(Pi);
	
		Entry main = db.getEntry(planner_module, Term.tuple( Term.sym("main"), Term.tuple(s0, g, O), exec_module ));

		StopWatch.start("Main (whitebox)");
		server.satisfyRequest(main, db, exec_module);
		StopWatch.stop("Main (whitebox)");
		
		Term pi = db.getEntry(exec_module, Term.sym("pi")).getValue();
	
//		Evaluator eval = ((Evaluator)fReg.getFunction(DefaultFunctions.EVAL));
//		Pi = eval.compute(Pi.resolve(db));
//		StopWatch.start("Main (blackbox)");
//		Term pi2 = fPlan.compute(Pi);
//		StopWatch.stop("Main (blackbox)");
//		
		

		if ( pi.equals(CommonTerm.NIL) ) {
			System.out.println("No plan found.");
		} else {
			System.out.println("Plan:");
			for ( Term a : pi.asList() ) {
				System.out.println("\t" + a);
			}
		}
		
//		if ( pi2.equals(CommonTerm.NIL) ) {
//			System.out.println("No plan found.");
//		} else {
//			System.out.println("Plan:");
//			for ( Term a : pi2.asList() ) {
//				System.out.println("\t" + a);
//			}
//		}
		
		System.out.println(StopWatch.allSums2Str());
		System.out.println(Profiler.getString());
	}

}
