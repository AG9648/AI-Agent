import sys # For system paths and configurations.
import os # For checking files and environment variables.

# Path Setup: Connecting the modules
sys.path.append(os.getcwd()) # Ensure Python searches the current directory for our modules.

from MCP_tools import tools # Import the data-fetching layer (Module 2).
from MCP_tools import repair_kit # Import the automated repair layer (Module 4).

# The Self-Auditing Agent Class (Module 3 - The 'Brain')
class SelfAuditAgent: # Create a class that makes decisions based on data.
    def __init__(self): # Initialize the agent.
        self.report = {} # Storage for our final findings and risk scores.

    # Main Function: Executes a full diagnostic cycle
    def run_audit(self): # Define the audit process.
        print("\n[Audit Agent] Running self-diagnostic sweep...") # Status update.

        # Fetch metrics using our safe Tools layer (Module 2)
        health = tools.get_current_model_health() # Get avg confidence and accuracy.
        drift = tools.check_feature_drift() # Get Z-score drift report.

        # Evaluation Logic: Converting numbers into labels
        issues = [] # List to accumulate detected problems.
        risk_score = 0 # Numerical indicator of how dangerous things are.

        # 1. Model Health Check (Confidence threshold < 0.6)
        conf = health.get('avg_confidence', 0) # Get confidence value.
        if conf < 0.6: # Check if it's below our 60% standard.
            issues.append(f"Confidence Crisis: {conf}") # Log the specific issue.
            risk_score += 40 # Add heavy penalty to the risk score.

        # 2. Feature Drift Check (Z-score > 2.0)
        if drift['status'] == 'success': # If we successfully analyzed drift...
            for feat, data in drift['drifts'].items(): # iterate through every feature.
                if data['z_score'] > 2.0: # If any feature's Z-score is over 2...
                    issues.append(f"Drift Detected: {feat} (Score: {data['z_score']})") # Record it.
                    risk_score += 20 # Add risk for every drifted feature found.

        # 3. Accuracy / Failure Check (Below 0.5)
        acc = health.get('accuracy', 0) # Read current model accuracy.
        if acc < 0.5: # If accuracy is below 50%...
            issues.append(f"High Failure Rate: {acc}") # Record it as a critical failure.
            risk_score += 50 # Add the highest risk penalty.

        # Status Selection: Based on total Risk Score
        if risk_score >= 70: # If the risk is extreme...
            status = "CRITICAL" # Mark as urgent repair needed.
        elif risk_score >= 30: # If there are notable issues...
            status = "WARNING" # Mark as needs monitoring.
        else: # if the score is low...
            status = "PASS" # Everything is healthy.

        # Save findings in the internal report object
        self.report = { # Create the report dictionary.
            "status": status, # Final verdict label.
            "risk_score": risk_score, # Final calculated danger number.
            "issues": issues, # List of everything we found wrong.
            "metrics": { "health": health, "drift": drift } # Reference to raw data.
        } # Close dictionary.

        # Auto-Repair: Triggering the fix
        if status == "CRITICAL": # If the situation is urgent...
            self.attempt_repair() # Try to fix the problem automatically.

        return self.report # Return the complete analysis for further use.

    
    # Action Logic: Calls the Repair Kit
    def attempt_repair(self): # Function triggered by the agent's decision.
        print("[Audit Agent] !!! CRITICAL FAIL !!! Requesting automated repair...") # Alert.
        success = repair_kit.perform_auto_repair() # Call the Module 4 repair tool.
        if success: # If the repair tool finished correctly...
            print("[Audit Agent] Repair successful. System status reset to monitoring.") # Log.
        else: # If the repair tool failed...
            print("[Audit Agent] Repair failed. Manual engineering intervention required.") # Alert.

# Demonstration: Running the code directly
if __name__ == "__main__": # Entry point for local testing.
    agent = SelfAuditAgent() # Create the agent.
    results = agent.run_audit() # Perform the audit.
    
    # Print the findings clearly
    print("\n--- FINAL SYSTEM REPORT ---") # Header.
    print(f"SYSTEM STATUS: {results['status']}") # Display status.
    print(f"TOTAL RISK: {results['risk_score']}/100") # Display score.
    print(f"PROBLEMS: {results['issues']}") # List issues.
    print("---------------------------\n") # Footer.
