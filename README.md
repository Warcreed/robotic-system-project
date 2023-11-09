# Robotic Manipulator Project
This is a robotic project for the academic course "Robotic Systems", IT department (DMI), UniCT.

The main goal is to collect all the objects in a specific color order —blue, green, then red— while avoiding obstacles. The system consists of three main components: the GUI and robot controller, the main declarative agent, and the block manager agent.

![Demo](docs/exec_example.gif)


## Installation

Install requirements by running:

### Step 1

Linux:

```bash
  $ ./init.sh
```

MacOs:

**NB:** [HomeBrew](https://brew.sh/) is required.

```bash
  $ ./init_macos.sh
```
### Step 2

Next install [PHIDIAS](https://github.com/corradosantoro/phidias) and you are good to go.

## Run the project

Run the following files in separate terminal instances: 

```bash
  $ python3 main_gui.py
```
`main_gui.py` runs the robot instance which waits for instructions by the phidias agents.

```bash
  $ python3 ./phidias_agents/phidias_main.py
```
`phidias_main.py` is the main agent. It talks via socket to the block manager agent and gives instructions to the robot.

```bash
  $ python3 ./phidias_agents/phidias_block_manager.py
```
`phidias_block_manager.py` talks via socket to the main agent to get the task done.

### Commands
Commands are accepted only by the **main agent console**. There are 2 main ones:

```
  eShell: main > generate(5)
```
- The `generate` command accepts values ​​in the range **[1, 6]**, other values will be dropped. It generates N blocks into the world in 10 specified positions.

```
  eShell: main > pick()
```
- The `pick` command does not accept values. It gives the robot istructions to scan the world and collects the blocks **in order (blue, green, red)**.