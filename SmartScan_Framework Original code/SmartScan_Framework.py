import networkx as nx
import subprocess
import os
import matplotlib.pyplot as plt

# Paths to required files and binaries
smv_file = "C:\\Users\\hp\\Documents\\2025 prjs\\Mrs. Soumya\\model.smv"
nuxmv_path = "C:\\Users\\hp\\Documents\\2025 prjs\\Mrs. Soumya\\nuXmv-2.1.0-win64\\nuXmv-2.1.0-win64\\bin\\nuXmv.exe"
command_file = "C:\\Users\\hp\\Documents\\2025 prjs\\Mrs. Soumya\\commands.txt"

# Step 1: Solidity to BIP Conversion
def solidity_to_bip(solidity_code):
    """Converts Solidity code to a BIP model."""
    functions = extract_functions(solidity_code)
    state_variables = extract_state_variables(solidity_code)
    control_flows = extract_control_flows(solidity_code)

    # Generate BIP model
    bip_model = {
        "functions": functions,
        "state_variables": state_variables,
        "control_flows": control_flows,
    }
    return bip_model

def extract_functions(solidity_code):
    """Extracts functions from Solidity code."""
    return ["deposit", "withdraw", "borrow", "repay"]

def extract_state_variables(solidity_code):
    """Extracts state variables from Solidity code."""
    return ["deposits", "debts", "collateralFactor"]

def extract_control_flows(solidity_code):
    """Extracts control flow structures from Solidity code."""
    return ["if", "require", "assert"]

# Step 2: BIP to FSM Conversion
def bip_to_fsm(bip_model):
    """Converts BIP model to FSM."""
    fsm = nx.DiGraph()

    states = ["Start", "FundsDeposited", "FundsWithdrawn", "FundsBorrowed", "FundsRepaid"]
    transitions = [
        ("Start", "FundsDeposited"),
        ("FundsDeposited", "FundsWithdrawn"),
        ("FundsDeposited", "FundsBorrowed"),
        ("FundsBorrowed", "FundsRepaid"),
    ]

    fsm.add_nodes_from(states)
    fsm.add_edges_from(transitions)

    return fsm

# Step 3: Symbolic Model Checking with NuXmv
def write_smv_file(fsm, ctl_properties, output_file="model.smv"):
    """Writes FSM and CTL properties to an SMV file."""
    with open(output_file, "w") as f:
        f.write("MODULE main\n")
        f.write("VAR\n")
        f.write(" state : {" + ", ".join(f'"{state}"' for state in fsm.nodes) + "};\n")
        f.write(" balance : integer;\n")
        f.write("ASSIGN\n")
        f.write(" init(state) := \"Start\";\n")
        f.write(" init(balance) := 0;\n")  # Initialize balance to 0

        # Define transitions using the case structure
        f.write(" next(state) := case\n")
        for edge in fsm.edges:
            f.write(f' state = "{edge[0]}" : "{edge[1]}";\n')
        f.write(" TRUE : state;\n")  # Default case to retain current state
        f.write(" esac;\n")

        # Update balance based on state transitions
        f.write(" next(balance) := case\n")
        f.write(' state = "Start" & next(state) = "FundsDeposited" : balance + 100;\n')
        f.write(' state = "FundsDeposited" & next(state) = "FundsWithdrawn" : balance - 50;\n')
        f.write(' state = "FundsBorrowed" & next(state) = "FundsRepaid" : balance + 50;\n')
        f.write(" TRUE : balance;\n")  # Default case to retain current balance
        f.write(" esac;\n")

        # Add CTL properties
        for prop_name, ctl in ctl_properties.items():
            f.write(f"\n-- {prop_name}\n")
            f.write(f"SPEC {ctl};\n")

def write_command_file(output_file="commands.txt"):
    """Writes commands to a file for NuXmv."""
    with open(output_file, "w") as f:
        f.write("go_bmc\n")
        f.write("check_ltlspec\n")

def run_nuxmv(smv_file, command_file):
    """Runs the NuXmv model checker on the provided SMV file using a command file."""
    if not os.path.exists(nuxmv_path):
        raise FileNotFoundError(f"nuXmv binary not found at {nuxmv_path}")
    try:
        result = subprocess.run([nuxmv_path, "-source", command_file, smv_file], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"NuXmv returned an error: {result.stderr}")
            return None
        return result.stdout
    except FileNotFoundError:
        print("NuXmv is not installed or not in PATH.")
        return None

# Step 4: Counterexample Analysis
def parse_counterexamples(nuxmv_output):
    """Parses counterexamples from NuXmv output."""
    if nuxmv_output and "-- specification" in nuxmv_output and "is false" in nuxmv_output:
        start = nuxmv_output.index("Counterexample")
        return nuxmv_output[start:]
    return "No counterexamples found."

# Step 5: Visualization
def visualize_fsm(fsm, filename="fsm_diagram.png"):
    """Visualizes the FSM using NetworkX and matplotlib."""
    pos = nx.spring_layout(fsm)
    nx.draw(fsm, pos, with_labels=True, node_size=3000, node_color="lightblue")
    nx.draw_networkx_edges(fsm, pos, edge_color="gray")
    plt.title("FSM Visualization")
    plt.savefig(filename)
    plt.show()

def visualize_state_transitions(fsm, filename2="state_transitions.png"):
    """Visualizes state transitions as a bar chart."""
    transitions = list(fsm.edges)
    transition_counts = {edge: transitions.count(edge) for edge in transitions}

    plt.bar(
        [f"{t[0]} → {t[1]}" for t in transition_counts.keys()],
        transition_counts.values(),
        color="skyblue"
    )
    plt.title("State Transition Frequencies")
    plt.xlabel("Transitions")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(filename2)
    plt.show()

# Example Usage
if __name__ == "__main__":
    solidity_code = """ 
    pragma solidity ^0.8.0;
    contract DeFiLending {
        mapping(address => uint256) public deposits;
        mapping(address => uint256) public debts;
        uint256 public constant collateralFactor = 150;
        function deposit() external payable {}
        function withdraw(uint256 amount) external {}
        function borrow(uint256 amount) external {}
        function repay() external payable {}
    }
    """

    # Convert Solidity code to BIP model
    bip_model = solidity_to_bip(solidity_code)
    fsm = bip_to_fsm(bip_model)

    # Define CTL properties for model checking
    ctl_properties = {
        "Fund Safety": "AG (state != \"FundsDeposited\" -> balance >= 0)",
        "Reentrancy Prevention": "AG (! (state = \"FundsWithdrawn\" & EX(state = \"FundsWithdrawn\")))",
    }

    # Write SMV file and command file, then run NuXmv
    write_smv_file(fsm, ctl_properties)
    write_command_file(command_file)
    nuxmv_output = run_nuxmv(smv_file, command_file)
    if nuxmv_output:
        print(nuxmv_output)
        counterexamples = parse_counterexamples(nuxmv_output)
        print("Counterexamples:", counterexamples)
    else:
        print("NuXmv execution failed.")

    # Visualize FSM and transitions
    visualize_fsm(fsm)
    visualize_state_transitions(fsm)
