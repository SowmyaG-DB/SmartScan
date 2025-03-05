SmartScan: Formal Verification Framework for Smart Contracts
Overview
SmartScan is a formal verification framework designed to detect 14 critical vulnerabilities in Solidity-based smart contracts. By leveraging Finite State Machine (FSM) modeling and Computation Tree Logic (CTL)-based formal verification, SmartScan ensures systematic security validation for blockchain applications.
This repository contains SmartScan implementations for detecting 14 vulnerabilities, including reentrancy, integer overflow, access control misconfigurations, and front-running attacks. The codebase is structured to allow researchers and developers to analyze, test, and improve smart contract security using formal methods.
Repository Structure
The repository is organized into the following directories:
SmartScan/
│── Reentrancy/
│── Integer_Overflow/
│── Access_Control_Misconfiguration/
│── Front_Running/
│── Timestamp_Dependence/
│── Unchecked_Call_Return/
│── Unprotected_SelfDestruct/
│── DelegateCall_Issues/
│── Denial_of_Service/
│── Short_Address_Attack/
│── Storage_Manipulation/
│── TX_Origin_Authentication/
│── Floating_Point_Precision/
│── Weak_Randomness/
│── README.md
Each folder contains:
•	Solidity smart contract code demonstrating the vulnerability.
•	FSM & BIP model files for formal verification.
•	SMV files for model checking using nuXmv.
•	Counterexample generation outputs for debugging detected vulnerabilities.
Installation & Setup
To use SmartScan for vulnerability detection, follow these steps:
1️⃣ Clone the Repository
git clone https://github.com/Sowmya/SmartScan.git
cd SmartScan
2️⃣ Install Required Dependencies
SmartScan requires nuXmv for model checking.
sudo apt update && sudo apt install nuXmv
3️⃣ Run SmartScan for a Specific Vulnerability
Navigate to a vulnerability folder and execute the verification process:
cd Reentrancy/
nuXmv reentrancy.smv
Usage Guide
•	Modify the Solidity contracts to test custom vulnerabilities.
•	Use nuXmv to verify CTL properties in .smv files.
•	Analyze counterexample outputs to understand security flaws.
Detected Vulnerabilities
SmartScan formally verifies the following vulnerabilities:
#	Vulnerability	Detection Method
1	Reentrancy Attack	FSM + CTL Model Checking
2	Integer Overflow	Symbolic Model Verification
3	Access Control Misconfiguration	FSM State Transition Analysis
4	Front-Running Attack	Execution Order Verification
5	Timestamp Dependence	Temporal Model Checking
6	Unchecked Call Return	Static Analysis + FSM
7	Unprotected SelfDestruct	Ownership & State Verification
8	DelegateCall Issues	Execution Path Analysis
9	Denial of Service (Gas Limit)	Computation Cost Model
10	Short Address Attack	Parameter Length Validation
11	Storage Manipulation	Unauthorized State Modification
12	TX Origin Authentication	Authentication Flow Analysis
13	Floating Point Precision Issues	Numeric Computation Verification
14	Weak Randomness	Entropy Source Analysis
Example: Running SmartScan on Reentrancy Attack
1.	Navigate to the Reentrancy/ folder.
2.	Open reentrancy.sol and review the vulnerable contract.
3.	Run SmartScan’s nuXmv verification: 
4.	nuXmv reentrancy.smv
5.	Check the output for vulnerability detection and counterexamples.
Research & Citation
SmartScan has been developed as part of academic research on smart contract security. If you use this repository in your work, please cite the following papers:
1.	Sowmya, G. and Sridevi, R. (2025). "SmartScan: A Comprehensive Framework for Efficient and Optimized Formal Verification of Complex Blockchain Smart Contracts." Journal of Theoretical and Applied Information Technology, 103(3), pp. 814-834. Available at: https://www.jatit.org/volumes/Vol103No3/4Vol103No3.pdf
2.	Sowmya, G. and Sridevi, R. (2025). "SmartScan in Action: A Comprehensive Framework for Formal Verification of Smart Contract Vulnerabilities." (Under Peer Review)
Contributions & Contact
•	Contributions are welcome! Feel free to submit pull requests or open issues for enhancements.
•	For inquiries, contact gonurusowmya@gmail.com.
License
This project is licensed under the MIT License, allowing open-source usage and modifications.

