from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

# ---------------------------------------------------------------------
# Agent 'block_manager'
# ---------------------------------------------------------------------

class generate_blocks(Procedure): pass

class gen(Reactor): pass
class block_slot_status(Reactor): pass
class block_slot_color(Reactor): pass

class new_block(Belief): pass

class block_slot(Belief): pass

def_vars('C', 'D', 'N', 'B', '_from')

class block_manager(Agent):
    def main(self):

      # reactor
      +gen(N)[{'from': _from}] >> [ show_line("\nRequest to generate ", N, " blocks from ", _from), generate_blocks(N)]
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


      # strategy
      generate_blocks() >> [ +new_block()[{'to': 'robot@127.0.0.1:6566'}] ]
      generate_blocks(0) >> [ ]
      generate_blocks(N) / (geq(N,0) & leq(N, 6)) >> [
        show_line("Generating block ", N, "..."),
        generate_blocks(), 
        "N = N - 1", 
        generate_blocks(N) ]
      generate_blocks(N) >> [ show_line("Attenzione! Numero di blocchi generabili [0, 6]")]
      # check block already generated 


agent_block_manager = block_manager()
agent_block_manager.start()

# block_slot(index, busy) busy parameter is determined during scansion
for i in range(10):
  agent_block_manager.assert_belief(block_slot(i, False))

PHIDIAS.run_net(globals(), 'http', 6767)
PHIDIAS.shell(globals())