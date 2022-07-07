import sys
sys.path.insert(0, './lib')

from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

class geometry(SingletonBelief): pass

# beliefs interpreted by the robot
class go_to(Belief): pass
class new_block(Belief): pass
class sense_distance(Belief): pass
class sense_color(Belief): pass

# beliefs sent by the robot
class target_got(Reactor): pass
class distance(Reactor): pass
class color(Reactor): pass
class pose(SingletonBelief): pass

class block(Belief): pass
class target(SingletonBelief): pass

class go(Procedure): pass
class gen_block(Procedure): pass
class sense(Procedure): pass
class scan(Procedure): pass
class _scan(Procedure): pass
class _scan_next(Procedure): pass
class goto_block(Procedure): pass

def_vars('X','Y','A','_A','D', 'W', 'Gap', 'C', 'N')

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):
        # commands
        go(X,Y,A) >> [ +go_to(X,Y,A)[{'to': 'robot@127.0.0.1:6566'}] ]
        gen_block() >> [ +new_block()[{'to': 'robot@127.0.0.1:6566'}] ]
        sense() >> [ +sense_distance()[{'to': 'robot@127.0.0.1:6566'}],
                     +sense_color()[{'to': 'robot@127.0.0.1:6566'}] ]

        # strategy
        gen_block(0) >> [ ]
        gen_block(N) >> [ gen_block(), "N = N - 1", gen_block(N) ]

        scan() / geometry(W,Gap) >> [ "X = W/2 + W + Gap", 
                                      go(X, 0.02, -90), 
                                      +target(X, 0.02) ]

        +target_got()[{'from': _A}] / target(X, Y) >> \
          [
              show_line('Reached Position ', X),
              sense()
          ]

        +distance(D)[{'from':_A}] / (target(X, Y) & lt(D,0.035)) >> [ show_line("Block found in position ", X),
                                                                      +block(X) ]

        +color(C)[{'from':_A}] / (target(X, Y) & block(X)) >> [ show_line("Color ", C, " sampled in position ", X),
                                                                -block(X),
                                                                +block(X, C),
                                                                _scan_next() ]
        +color(C)[{'from':_A}] >> [ _scan_next() ]
        +color()[{'from':_A}] >> [ _scan_next() ]

        _scan_next() / (target(X, Y) & gt(X,0.3)) >> \
          [
              show_line('end')
          ]
        _scan_next() / (target(X, Y) & geometry(W, Gap)) >> \
          [
              "X = X + W + Gap", +target(X, Y),
              go(X, Y, -90)
          ]

        goto_block(C) / block(X,C) >> [ go(X, 0.02, -90),
                                        +target(X, 0.02) ]



ag = main()
ag.start()
ag.assert_belief(geometry(0.03, 0.01))
PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())

