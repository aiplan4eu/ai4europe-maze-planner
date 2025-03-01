from aiddl_core.container.container import Container
from aiddl_core.representation.sym import Sym
from aiddl_core.representation import Boolean
from aiddl_core.representation import Int
from aiddl_core.representation import Tuple
from aiddl_core.representation import KeyVal
from aiddl_core.representation import Set


FREE = Sym("free")
WALL = Sym("wall")
BOX = Sym("box")
AGENT = Sym("agnt")
A1 = Sym("a1")
A2 = Sym("a2")
A3 = Sym("a3")
A4 = Sym("a4")
A5 = Sym("a5")

S1 = Tuple([Sym("S"), A1])
S2 = Tuple([Sym("S"), A2])
S3 = Tuple([Sym("S"), A3])
S4 = Tuple([Sym("S"), A4])
S5 = Tuple([Sym("S"), A5])

G1 = Tuple([Sym("G"), A1])
G2 = Tuple([Sym("G"), A2])
G3 = Tuple([Sym("G"), A3])
G4 = Tuple([Sym("G"), A4])
G5 = Tuple([Sym("G"), A5])

term_map = [FREE, WALL, BOX, A1, G1, A2, G2, A3, G3, A4, G4, A5, G5]


class Region:
    def __init__(self, dim):
        self.dim = dim
        self.m = []
        self.cells = []
        self.start_map = {}
        self.goal_map = {}
        self.pos_map = {}
        for i in range(dim):
            row = []
            for j in range(dim):
                row.append(FREE)
            self.m.append(row)

    def to_goal(self):
        state = set()
        for (i, j) in self.goal_map.keys():
            value = self.goal_map[(i, j)][1]
            state.add(
                    KeyVal(
                        Tuple([
                            Sym("at"),
                            value,
                            Tuple(
                                [Int(i),
                                 Int(j)])]),
                        Sym("true")))
        return Set(state)

    def get_state_and_goal(self):
        state = set()
        goal = set()
        for i in range(self.dim):
            for j in range(self.dim):
                if j > 0:
                    state.add(KeyVal(Tuple([Sym("N"),
                                              Sym("x%dy%d" % (i, j-1)),
                                              Sym("x%dy%d" % (i, j))]),
                                       Sym("true")))
                if j < (self.dim-1):
                    state.add(KeyVal(Tuple([Sym("S"),
                                              Sym("x%dy%d" % (i, j+1)),
                                              Sym("x%dy%d" % (i, j))]),
                                       Sym("true")))
                if i > 0:
                    state.add(KeyVal(Tuple([Sym("W"),
                                              Sym("x%dy%d" % (i-1, j)),
                                              Sym("x%dy%d" % (i, j))]),
                                       Sym("true")))
                if i < (self.dim-1):
                    state.add(KeyVal(Tuple([Sym("E"),
                                              Sym("x%dy%d" % (i+1, j)),
                                              Sym("x%dy%d" % (i, j))]),
                                       Sym("true")))

                value = self.m[i][j]
                if value in set({G1, G2, G3, G4, G5}):
                    if value == G1:
                        goal_agent = A1
                    elif value == G2:
                        goal_agent = A2
                    elif value == G3:
                        goal_agent = A3
                    elif value == G4:
                        goal_agent = A4
                    else:
                        goal_agent = A5
                    goal.add(
                        KeyVal(
                            Tuple([
                                Sym("at"),
                                goal_agent,
                                Sym("x%dy%d" % (i, j))]),
                            Sym("true")))
                    value = FREE
                if value in set([A1, A2, A3, A4, A5]):
                    state.add(
                        KeyVal(
                            Tuple([
                                Sym("at"),
                                value,
                                Sym("x%dy%d" % (i, j))]),
                            Sym("true")))

                    value = Sym("agnt")
                    
                state.add(
                    KeyVal(
                        Tuple(
                            [Sym("map"),
                             Sym("x%dy%d" % (i, j)),
                             value]),
                        Sym("true")))

                    
        print("State:", Set(state))
        print("Goal: ", Set(goal))
              
        return (Set(state), Set(goal))


def get_full_action(a, O):
    for o in O:
        s = o[Sym("name")].match(a)
        if s is not None:
            print(s, a, o)
            return o.substitute(s)
    print("Error: Action %s has no matching operator in:" % str(a))
    for o in O:
        print("\t", o)
    return None


def state_transition(s, a):
    return s.put_all(a[Sym("effects")])
