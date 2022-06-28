from collections import OrderedDict

# Load AIDDL core
from aiddl_core.parser.parser import parse
from aiddl_core.representation import Sym
from aiddl_core.representation import Boolean
from aiddl_core.representation import Set
from aiddl_core.representation.sym import TRUE
from aiddl_core.representation.sym import FALSE
import aiddl_core.function.default as dfun
from aiddl_core.function.uri import EVAL
from aiddl_core.container.container import Container
from aiddl_core.tools.logger import Logger

# Load UP
import unified_planning
from unified_planning.shortcuts import *

def get_obj_or_param(t, obj_map, param_map):
    if t in obj_map.keys():
        return obj_map[t]
    elif t in param_map.keys():
        return param_map[t]
    else:
        print("Paramter or object not found: %s" % (t))


def aiddl_svp_2_up(aiddl, name):
    state_aiddl = aiddl[Sym("initial-state")]
    goal_aiddl = aiddl[Sym("goal")]
    operators_aiddl = aiddl[Sym("operators")]
    domains_aiddl = aiddl[Sym("domains")]
    sig_aiddl = aiddl[Sym("signatures")]

    #print("--------------------------------------------------------------------------------")
    #print("INPUT AIDDL:")
    #print("--------------------------------------------------------------------------------")
    #print(Logger.pretty_print(state_aiddl, 0))
    #print(Logger.pretty_print(goal_aiddl, 0))
    #print(Logger.pretty_print(operators_aiddl, 0))
    #print(Logger.pretty_print(domains_aiddl, 0))


    up_problem = Problem(name)

    type_map = {}
    obj_map = {}
    fluent_map = {}

    print("Converting domains...")
    for d in domains_aiddl:
        if d.get_value() == Set([Boolean(True), Boolean(False)]):
            type_map[d.get_key()] = BoolType()
            obj_map[Boolean(True)] = TRUE()
            obj_map[Boolean(False)] = FALSE()
        else:
            up_type = UserType(str(d.get_key()))
            type_map[d.get_key()] = up_type
            up_objects = []
            for o in d.get_value():
                up_obj = Object(str(o), up_type)
                if o not in obj_map.keys():
                    obj_map[o] = up_obj
                    up_objects.append(up_obj)

            up_problem.add_objects(up_objects)

    print("Converting signatures...")
    for s in sig_aiddl:
        param_idx = 1
        fluent_name = str(s.get_key()[0])
        val_type = type_map[s.get_value()]
        #print("Fluent: %s Type: %s" % (fluent_name, val_type))
        
        params_aiddl = [s.get_key()[i] for i in range(1, len(s.get_key()))]
        params = OrderedDict()
        for x in params_aiddl:
            params["%s_%d" % (x, param_idx)] = type_map[x]
            param_idx += 1
            # params = [str(x)type_map[x] for x in params_aiddl]
        #print("Creating fluent...")
        #print(type(val_type))
        #for t in params:
        #    print(t, type(t))
        
        if s.get_value() == Sym("boolean"):
            f = Fluent(fluent_name, val_type, params)
        else:
            f = Fluent(fluent_name, val_type, params)
        #print(f)
        up_problem.add_fluent(f, default_initial_value=False)
        fluent_map[s.get_key()[0]] = f

        print("Adding fluent:", f)
        print(params)
        for p in params:
            print(p, type(p))

    print("Converting state...") # TODO: CONTINUE HERE
    for s in state_aiddl:
        f = fluent_map[s.get_key()[0]]
        params_aiddl = [s.get_key()[i] for i in range(1, len(s.get_key()))]
        params = tuple([obj_map[x] for x in params_aiddl])
        value = obj_map[s.get_value()]

        #print("Fluent:", f)
        #print(params)
        #print(value)

        up_problem.set_initial_value(f(*params), value)

    print("Converting goals...")
    for s in goal_aiddl:
        f = fluent_map[s.get_key()[0]]
        params_aiddl = [s.get_key()[i] for i in range(1, len(s.get_key()))]
        args = tuple([obj_map[x] for x in params_aiddl])
        value = obj_map[s.get_value()]
        if s.get_value() == Boolean(True):
            expr = f(*args)
        elif s.get_value() == Boolean(False):
            expr = Not(f(*args))
        else:
            right = get_obj_or_param(s.get_value(), obj_map, {})
            left = f(*args)
            expr = Equals(left, right)
        up_problem.add_goal(expr)


    print("Converting operators...")
    for a in operators_aiddl:
        name = a[Sym("name")][0]
        sig = OrderedDict()
        for i in range(len(a[Sym("signature")])):
            t = type_map[a[Sym("signature")][i]]
            p = str(a[Sym("name")][i+1]).replace("?", "")
            sig[p] = t
        #print(sig)
        action = InstantaneousAction(str(name), sig)
        param_map = {}
        for i in range(1, len(a[Sym("name")])):
            p = a[Sym("name")][i]
            param = action.parameter(str(p).replace("?", ""))
            param_map[p] = param

        for cond in a[Sym("preconditions")]:
            f = fluent_map[cond.get_key()[0]]
            args = tuple([get_obj_or_param(cond.get_key()[i], obj_map, param_map) for i in range(1, len(cond.get_key()))])

            
            if cond.get_value() == Boolean(True):
                expr = f(*args)
            elif cond.get_value() == Boolean(False):
                expr = Not(f(*args))
            else:
                right = get_obj_or_param(cond.get_value(), obj_map, param_map)
                left = f(*args)
                expr = Equals(left, right)
            #print(cond, "->", expr, type(cond.get_value()), cond.get_value() == Boolean(True)) 
            action.add_precondition(expr)

        for eff in a[Sym("effects")]:
            f = fluent_map[eff.get_key()[0]]
            args = tuple([get_obj_or_param(eff.get_key()[i], obj_map, param_map) for i in range(1, len(eff.get_key()))])
            if eff.get_value() == Boolean(True):
                right = True
            elif eff.get_value() == Boolean(False):
                right = False
            else:
                right = get_obj_or_param(eff.get_value(), obj_map, param_map)
            left = f(*args)
            action.add_effect(left, right)

        up_problem.add_action(action)
    return up_problem



