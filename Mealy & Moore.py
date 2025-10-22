# Mealy and Moore Machine for detecting '01' sequence
# Outputs 'a' when '01' occurs, else 'b'

# -----------------------------
# ASCII DIAGRAMS
# -----------------------------
MEALY_ASCII = (
    "\n======================\n"
    "   MEALY MACHINE\n"
    "======================\n"
    "\n(Outputs 'a' when '01' occurs, else 'b')\n\n"
    "                          ┌───────────────┐\n"
    "                 1/b  ↺   │       A       │─────0/b────▶│       B       │\n"
    "                    ◀─────┘   (start)     │             │               │\n"
    "                           └──────────────┘             └─────┬─────────┘\n"
    "                                                               │\n"
    "                                                               │\n"
    "                                                               │1/a\n"
    "                                                               ▼\n"
    "                                                         ┌───────────────┐\n"
    "                                                         │       C       │\n"
    "                                                         └─────┬─────────┘\n"
    "                                                               │\n"
    "                                                               │0/b\n"
    "                                                               ▼\n"
    "                                                         ┌───────────────┐\n"
    "                                                         │       A       │\n"
    "                                                         └───────────────┘\n"
    "\n(Transitions are labeled as input/output)\n"
)

MOORE_ASCII = (
    "\n======================\n"
    "   MOORE MACHINE\n"
    "======================\n"
    "\n(Outputs 'a' in state C, which indicates '01' was seen)\n\n"
    "                          ┌───────────────┐\n"
    "                 1        │       A       │─────0────▶│       B       │\n"
    "                    ◀─────┘   (start,b)   │           │   (b)         │\n"
    "                           └──────────────┘           └─────┬─────────┘\n"
    "                                                             │\n"
    "                                                             │1\n"
    "                                                             ▼\n"
    "                                                       ┌───────────────┐\n"
    "                                                       │       C       │\n"
    "                                                       │     (a)       │\n"
    "                                                       └─────┬─────────┘\n"
    "                                                             │\n"
    "                                                             │0\n"
    "                                                             ▼\n"
    "                                                       ┌───────────────┐\n"
    "                                                       │       A       │\n"
    "                                                       │     (b)       │\n"
    "                                                       └───────────────┘\n"
)

# -----------------------------
# MACHINE CLASSES (different internal structure)
# -----------------------------
class MealyMachine:
    def __init__(self):
        # transitions represented as tuples (next_state, output)
        self._trans = {
            ('A', '0'): ('B', 'b'),
            ('A', '1'): ('A', 'b'),
            ('B', '0'): ('B', 'b'),
            ('B', '1'): ('C', 'a'),
            ('C', '0'): ('A', 'b'),
            ('C', '1'): ('C', 'b'),
        }
        self.start = 'A'

    def step(self, state, symbol):
        return self._trans[(state, symbol)]


class MooreMachine:
    def __init__(self):
        # transitions map (state, input) -> next_state; outputs per-state
        self._trans = {
            ('A', '0'): 'B',
            ('A', '1'): 'A',
            ('B', '0'): 'B',
            ('B', '1'): 'C',
            ('C', '0'): 'A',
            ('C', '1'): 'C',
        }
        self._out = {'A': 'b', 'B': 'b', 'C': 'a'}
        self.start = 'A'

    def step(self, state, symbol):
        return self._trans[(state, symbol)]

    def out(self, state):
        return self._out[state]


# -----------------------------
# PRINT DIAGRAMS
# -----------------------------
print(MEALY_ASCII)
print(MOORE_ASCII)

# -----------------------------
# SIMULATION FUNCTIONS
# -----------------------------
def _numbered_output(output_string):
    return " ".join(f"{i+1}:{ch}" for i, ch in enumerate(output_string))

def simulate_mealy(input_string, machine):
    current_state = machine.start
    output_string = ""
    
    # Collect all step data
    states = []
    inputs = []
    nexts = []
    outputs = []
    
    for symbol in input_string:
        next_state, output = machine.step(current_state, symbol)
        states.append(current_state)
        inputs.append(symbol)
        nexts.append(next_state)
        outputs.append(output)
        output_string += output
        current_state = next_state
    
    # Print header
    print(f"\n--- MEALY SIMULATION for input: {input_string} ---")
    
    # Print transposed table
    steps = "Step:  " + "  ".join(f"{i+1:<3}" for i in range(len(input_string)))
    state_row = "State: " + "  ".join(f"{s:<3}" for s in states)
    input_row = "Input: " + "  ".join(f"{i:<3}" for i in inputs)
    next_row = "Next:  " + "  ".join(f"{n:<3}" for n in nexts)
    output_row = "Output:" + "  ".join(f"{o:<3}" for o in outputs)
    
    print(steps)
    print(state_row)
    print(input_row)
    print(next_row)
    print(output_row)
    
    print(f"\nFinal Output: {output_string}\n")
    print(f"Numbered Output: {_numbered_output(output_string)}\n")


def simulate_moore(input_string, machine):
    current_state = machine.start
    output_string = machine.out(current_state)
    
    # Collect all step data
    states = []
    inputs = []
    nexts = []
    outputs = []
    
    for symbol in input_string:
        next_state = machine.step(current_state, symbol)
        states.append(current_state)
        inputs.append(symbol)
        nexts.append(next_state)
        outputs.append(machine.out(next_state))
        output_string += machine.out(next_state)
        current_state = next_state
    
    # Print header
    print(f"\n--- MOORE SIMULATION for input: {input_string} ---")
    
    # Print transposed table
    steps = "Step:  " + "  ".join(f"{i+1:<3}" for i in range(len(input_string)))
    state_row = "State: " + "  ".join(f"{s:<3}" for s in states)
    input_row = "Input: " + "  ".join(f"{i:<3}" for i in inputs)
    next_row = "Next:  " + "  ".join(f"{n:<3}" for n in nexts)
    output_row = "Output:" + "  ".join(f"{o:<3}" for o in outputs)
    
    print(steps)
    print(state_row)
    print(input_row)
    print(next_row)
    print(output_row)
    
    print(f"\nFinal Output: {output_string}\n")
    print(f"Numbered Output: {_numbered_output(output_string)}\n")


# -----------------------------
# RUN SIMULATIONS
# -----------------------------
mealy = MealyMachine()
moore = MooreMachine()

inputs = ["011001", "110011"]

for inp in inputs:
    simulate_mealy(inp, mealy)
    simulate_moore(inp, moore)
