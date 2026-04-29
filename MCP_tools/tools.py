import csv # Import for reading and writing comma-separated value files.
import os # Import for interacting with the computer's file system.
import pandas as pd # Import for advanced data manipulation and statistics.
import numpy as np # Import for heavy numerical calculations.

# Configuration: Pointing to where our data lives
PREDICTIONS_FILE = "data/predictions.csv" # The file where we record every live prediction.
REFERENCE_FILE = "data/reference_data.csv" # The file containing our 'perfect' training data.

# Tool 1: Get Recent History
def get_recent_predictions(limit=50): # Function to fetch the most recent data points.
    """ # Documentation start.
    Reads the last N rows from the prediction log file. # Simplified role of function.
    """ # Documentation end.
    if not os.path.exists(PREDICTIONS_FILE): # Check if the file actually exists.
        return [] # Return an empty list if there's no file yet.
    
    df = pd.read_csv(PREDICTIONS_FILE) # Load the whole history into a pandas DataFrame.
    recent_data = df.tail(limit) # Slice the table to get only the last 'limit' number of rows.
    return recent_data.to_dict(orient='records') # Convert the table rows into easy-to-read dictionaries.

# Tool 2: Get Baseline Stats
def get_ref_data_stats(): # Function to calculate the 'standard' or 'normal' data range.
    """ # Documentation start.
    Calculates average and spread for the original training/reference data. # Role.
    """ # Documentation end.
    if not os.path.exists(REFERENCE_FILE): # Check if we have original data to compare against.
        return None # Return None if no baseline data is found.
    
    df = pd.read_csv(REFERENCE_FILE) # Load the reference dataset.
    feature_cols = ['f0', 'f1', 'f2', 'f3', 'f4'] # Identify the 5 features we want to track.
    stats = { # Create a dictionary to hold the results.
        'mean': df[feature_cols].mean().to_dict(), # Calculate the average for each feature.
        'std': df[feature_cols].std().to_dict() # Calculate the standard deviation/variation for each.
    } # Close dictionary.
    return stats # Return the calculated stats back to the requester.

# Tool 3: Measure Current Health
def get_current_model_health(): # Function to see how well the AI is performing right now.
    """ # Documentation start.
    Calculates accuracy and confidence averages from recent history. # Role.
    """ # Documentation end.
    if not os.path.exists(PREDICTIONS_FILE): # check if there is any history to analyze.
        return {"avg_confidence": 0, "accuracy": 0} # Return zeros if no data is found.
    
    df = pd.read_csv(PREDICTIONS_FILE) # Read the entire history of predictions.
    if df.empty: # Check if the file is empty (has headers but no rows).
        return {"avg_confidence": 0, "accuracy": 0} # Return zeros if empty.
    avg_conf = df['confidence'].mean() # Calculate the mathematical average of confidence scores.
    
    # Check Accuracy (Comparing predicted value vs ground truth/actual answer)
    valid_data = df.dropna(subset=['ground_truth']) # Filter out rows where we don't know the real answer yet.
    if not valid_data.empty: # If we have at least one verified prediction...
        correct = (valid_data['prediction'] == valid_data['ground_truth']).sum() # Count matches.
        accuracy = correct / len(valid_data) # Divide correct counts by total count for percentage.
    else: # If we have no ground truth data yet...
        accuracy = 0.0 # Set accuracy to zero.
    return { # Prepare the health report.
        "avg_confidence": round(float(avg_conf), 4), # Return confidence rounded for neatness.
        "accuracy": round(float(accuracy), 4) # Return accuracy rounded for neatness.
    } # Close dictionary.

# Tool 4: Detect Data Drift (Z-Score method)
def check_feature_drift(): # Function to see if incoming data has 'drifted' or changed too much.
    """ # Documentation start.
    Compares live data patterns against historical baselines using Z-Scores. # Role.
    """ # Documentation end.
    ref_stats = get_ref_data_stats() # Get the 'normal' stats from Tool 2.
    recent_logs = get_recent_predictions(limit=100) # Get the last 100 predictions to check.
    
    if not ref_stats or not recent_logs: # If we are missing either history or live data...
        return {"status": "insufficient_data", "drifts": {}} # Report that we need more data.
    
    recent_df = pd.DataFrame(recent_logs) # Convert the recent predictions into a data table.
    feature_cols = ['f0', 'f1', 'f2', 'f3', 'f4'] # List the features to analyze for changes.
    drift_report = {} # Storage for the final results per feature.
    
    for feat in feature_cols: # Loop through every feature one by one.
        live_mean = recent_df[feat].mean() # Find out what the 'average' looks like right now.
        ref_mean = ref_stats['mean'][feat] # Retrieve what the 'average' was during training.
        ref_std = ref_stats['std'][feat] # Retrieve how much variation was allowed during training.
        
        if ref_std == 0: z_score = 0 # Avoid mathematical error if there was zero variation.
        else: z_score = abs((live_mean - ref_mean) / ref_std) # Standard Z-Score formula calculation.
        
        drift_report[feat] = { # Save the result for this specific feature.
            "z_score": round(z_score, 4), # Record how many 'deviations' away the new data is.
            "is_drifted": bool(z_score > 3.0) # Mark as drifted if the score is very high (> 3).
        } # End per-feature storage.
        
    return { # Pack it up.
        "status": "success", # Status message.
        "drifts": drift_report # The feature-by-feature report.
    } # Close dictionary.