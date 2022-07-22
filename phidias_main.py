import sys
sys.path.insert(0, './lib')

from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

class mode(SingletonBelief): pass

# beliefs interpreted by the robot
class go_to_block_slot(Belief): pass
class go_to(Belief): pass
class sense_block_presence(Belief): pass
class sense_color(Belief): pass

# beliefs interpreted by the block_manager
class gen(Reactor): pass
class block_slot_status(Reactor): pass
class block_slot_color(Reactor): pass

# beliefs sent by the robot
class target_got(Reactor): pass
class is_block_present(Reactor): pass
class color(Reactor): pass

class target(SingletonBelief): pass

class go(Procedure): pass
class generate(Procedure): pass
class pick(Procedure): pass
class scan(Procedure): pass
class _scan_block_slot(Procedure): pass

def_vars('X','Y','A','_from','D', 'W', 'Gap', 'C', 'N', 'M', 'B')

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):

      # commands
      generate(N) >> [ +gen(N)[{'to': 'block_manager@127.0.0.1:6767'}] ]

      pick() >> []

      # comandi ausiliari
      scan() >> [ +mode("scanning"), _scan_block_slot(0) ]
      go(X) >> [ +go_to_block_slot(X)[{'to': 'robot@127.0.0.1:6566'}] ]
      go(X,Y,A) >> [ +go_to(X,Y,A)[{'to': 'robot@127.0.0.1:6566'}] ]


      # strategy

      ## scanning
      _scan_block_slot(10) >> [ show_line("Fine scansione"), +mode("")]
      _scan_block_slot(N) >> [ go(N), +target(N) ]

      +target_got()[{'from': _from}] / (target(N) & mode(M) & eq(M, "scanning")) >> [
        show_line('Reached Target ', N),
        +sense_block_presence()[{'to': 'robot@127.0.0.1:6566'}]
      ]

      +is_block_present(True)[{'from': _from}] / target(N) >> [
        +block_slot_status(N, B)[{'to': 'block_manager@127.0.0.1:6767'}],
        +sense_color()[{'to': 'robot@127.0.0.1:6566'}]
      ]

      +is_block_present(False)[{'from': _from}] / target(N) >> [
        +block_slot_status(N, B)[{'to': 'block_manager@127.0.0.1:6767'}],
        "N=N+1",
        _scan_block_slot(N)
      ]

      +color(C)[{'from':_from}] / target(N) >> [ 
        show_line("Color ", C, " sampled in position ", N),
        +block_slot_color(N, C)[{'to': 'block_manager@127.0.0.1:6767'}],
        "N=N+1",
        _scan_block_slot(N)
      ]

main().start()

PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())

