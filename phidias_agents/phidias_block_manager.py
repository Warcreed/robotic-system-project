from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

# ---------------------------------------------------------------------
# Agent 'blocks_manager'
# ---------------------------------------------------------------------

class generate_blocks(Procedure): pass
class _pick_block(Procedure): pass

# reactors sent by main agent
class gen(Reactor): pass
class block_slot_status(Reactor): pass
class block_slot_color(Reactor): pass
class pick_block(Reactor): pass

# beliefs interpreted by the robot
class new_block(Belief): pass

# intern beliefs used by blocks_manager
class block_slot(Belief): pass

# beliefs interpreted by the main agent
class pick_block_at(Reactor): pass
class no_more_blocks(Reactor): pass

def_vars('_from', 'N', 'B', 'D', 'C')

class blocks_manager(Agent):
    def main(self):

      # generating blocks
      +gen(N)[{'from': _from}] / (geq(N,1) & leq(N, 6)) >> [ show_line("\nRequest to generate ", N, " blocks from ", _from), generate_blocks(N)]
      
      generate_blocks() >> [ +new_block()[{'to': 'robot@127.0.0.1:6566'}] ]
      generate_blocks(0) >> [ ]
      generate_blocks(N) / (geq(N,1) & leq(N, 6)) >> [
        show_line("Generating block ", N, "..."),
        generate_blocks(), 
        "N = N - 1", 
        generate_blocks(N) ]
      generate_blocks(N) >> [ show_line("Attenzione! Numero di blocchi generabili [1, 6]") ]
      # check block already generated 

      # scanning blocks
      +block_slot_status(N, B)[{'from': _from}] / block_slot(N, D) >> [
        -block_slot(N, D),
        +block_slot(N, B),
        show_line("\nBlock Slot ", N, " status updated from ", D, " to ", B)
      ]

      +block_slot_color(N, C)[{'from': _from}] / block_slot(N, D) >> [
        -block_slot(N, D),
        +block_slot(N, D, C),
        show_line("Block Slot ", N, " color ", C, " set")
      ]

      # picking blocks
      +pick_block()[{'from': _from}] / block_slot(N, True, 'blue') >> [
        _pick_block(N, 'blue')
      ]
      +pick_block()[{'from': _from}] / block_slot(N, True, 'green') >> [
        _pick_block(N, 'green')
      ]
      +pick_block()[{'from': _from}] / block_slot(N, True, 'red') >> [
        _pick_block(N, 'red')
      ]

      _pick_block(N, C) >> [
        show_line("\nRequested block: sending block in slot ", N, " color ", C),
        -block_slot(N, True, C),
        +block_slot(N, False),
        +pick_block_at(N)[{'to': 'main@127.0.0.1:6565'}]
      ]

      +pick_block()[{'from': _from}] >> [
        show_line("\nNo more blocks in stock"),
        +no_more_blocks()[{'to': 'main@127.0.0.1:6565'}]
      ]

agent_blocks_manager = blocks_manager()
agent_blocks_manager.start()

# block_slot(index, busy) busy parameter is determined during scansion
for i in range(10):
  agent_blocks_manager.assert_belief(block_slot(i, False))

PHIDIAS.run_net(globals(), 'http', 6767)
PHIDIAS.shell(globals())