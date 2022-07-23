import sys
sys.path.insert(0, './lib')

from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

class mode(SingletonBelief): pass
class bowl_target_pos(SingletonBelief): pass

# beliefs interpreted by the robot
class go_to_block_slot(Belief): pass
class go_to(Belief): pass
class sense_block_presence(Belief): pass
class sense_color(Belief): pass
class collect_block(Reactor): pass
class drop_block(Reactor): pass

# beliefs interpreted by the block_manager agent
class gen(Reactor): pass
class block_slot_status(Reactor): pass
class block_slot_color(Reactor): pass
class pick_block(Reactor): pass

# beliefs sent by the robot
class target_got(Reactor): pass
class is_block_present(Reactor): pass
class color(Reactor): pass
class block_collected(Reactor): pass
class block_dropped(Reactor): pass

# beliefs sent by the block_manager agent
class pick_block_at(Reactor): pass
class no_more_blocks(Reactor): pass

class target(SingletonBelief): pass

class go(Procedure): pass
class generate(Procedure): pass
class pick(Procedure): pass
class scan(Procedure): pass
class _scan_block_slot(Procedure): pass
class _pick_blocks(Procedure): pass
class sense(Procedure): pass

def_vars('X','Y','A','_from','D', 'W', 'Gap', 'C', 'N', 'M', 'B')

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):

      # commands
      generate(N) >> [ 
        show_line("Requesting generation of ", N, " blocks"),
        +gen(N)[{'to': 'block_manager@127.0.0.1:6767'}] 
      ]

      pick() >> []

      # comandi ausiliari
      scan() >> [ +mode("scanning"), _scan_block_slot(0) ]
      go(X) >> [ +go_to_block_slot(X)[{'to': 'robot@127.0.0.1:6566'}] ]
      go(X,Y,A) >> [ +go_to(X,Y,A)[{'to': 'robot@127.0.0.1:6566'}] ]

      sense() >> [+sense_block_presence()[{'to': 'robot@127.0.0.1:6566'}]]
      # strategy

      ## scanning
      _scan_block_slot(10) >> [ show_line("Fine scansione\n"), +mode(""), go(0.1, 0.15, -90)]
      _scan_block_slot(N) >> [ go(N), +target(N) ]

      +target_got()[{'from': _from}] / (target(N) & mode(M) & eq(M, "scanning")) >> [
        show_line('\nReached Target ', N),
        +sense_block_presence()[{'to': 'robot@127.0.0.1:6566'}]
      ]

      +is_block_present(True)[{'from': _from}] / target(N) >> [
        show_line("Block is present at position  ", N),
        +block_slot_status(N, True)[{'to': 'block_manager@127.0.0.1:6767'}],
        +sense_color()[{'to': 'robot@127.0.0.1:6566'}]
      ]

      +is_block_present(False)[{'from': _from}] / target(N) >> [
        show_line("Block is NOT present at position  ", N),
        +block_slot_status(N, False)[{'to': 'block_manager@127.0.0.1:6767'}],
        "N=N+1",
        _scan_block_slot(N)
      ]

      +color(C)[{'from':_from}] / target(N) >> [ 
        show_line("Color ", C, " sampled in position ", N),
        +block_slot_color(N, C)[{'to': 'block_manager@127.0.0.1:6767'}],
        "N=N+1",
        _scan_block_slot(N)
      ]

      # picking block

      _pick_blocks() >> [
        show_line('\nStart collecting block in order (blue, green, red): '),
        +mode("collecting"), 
        +pick_block()[{'to': 'block_manager@127.0.0.1:6767'}] 
      ]

      +pick_block_at(N)[{'from':_from}] >> [ go(N), +target(N)]

      +target_got()[{'from': _from}] / (target(N) & mode(M) & eq(M, "collecting")) >> [
        show_line('\nReached Target ', N),
        +collect_block()[{'to': 'robot@127.0.0.1:6566'}]
      ]

      +block_collected()[{'from': _from}] / bowl_target_pos(X, Y, A) >> [
        +mode("dropping"),
        go(X, Y, A),
      ]

      +target_got()[{'from': _from}] / (mode(M) & eq(M, "dropping")) >> [
        show_line('\nReached bowl target: dropping block...'),
        +drop_block()[{'to': 'robot@127.0.0.1:6566'}]
      ]

      +block_dropped()[{'from': _from}] / target(N) >> [
        show_line('\nBlock dropped successfully! Requesting next block...'),
        +block_slot_status(N, False)[{'to': 'block_manager@127.0.0.1:6767'}],
        +mode("collecting"), 
        +pick_block()[{'to': 'robot@127.0.0.1:6566'}]
      ]

      +no_more_blocks()[{'from':_from}] >> [
        show_line("All blocks collected!"),
        +mode('')
      ]

agent_main = main()
agent_main.start()
agent_main.assert_belief(bowl_target_pos(0.07, 0.09, -90))

PHIDIAS.run_net(globals(), 'http', 6565)
PHIDIAS.shell(globals())

