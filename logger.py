import csv # Import the csv module to handle CSV file operations.
import os # Import the os module for interacting with the operating system file paths.
from datetime import datetime # Import the datetime class to capture current date and time.

# Global variable to store the path of the CSV log file
LOG_FILE = "data/predictions.csv" # The relative path where prediction data will be stored.

# Function to setup the logging file
def initialize_log(): # Define a function named initialize_log with no parameters.
    """ # Start of the function's docstring for documentation.
    This function creates a fresh CSV file with headers if it doesn't exist. # Explanation of function goal.
    """ # End of the function's docstring.
    if not os.path.exists('data'): # Check if the 'data' directory does not exist yet.
        os.makedirs('data') # Create the 'data' directory if it was missing.
        print("Created 'data' directory.") # Print a confirmation message to the console.
    
    # List of column names for the CSV file headers
    headers = [ # Start defining the headers list.
        'timestamp', # Column 1: stores the date and time of prediction.
        'f0', 'f1', 'f2', 'f3', 'f4', # Columns 2-6: stores the input features (f0 to f4).
        'prediction', # Column 7: stores the value predicted by the model.
        'confidence', # Column 8: stores the model's confidence score (0 to 1).
        'model_version', # Column 9: stores which version of the model was used.
        'ground_truth' # Column 10: stores the actual true value if available.
    ] # End of the headers list definition.

    # Create or overwrite the CSV file with the header row
    with open(LOG_FILE, mode='w', newline='') as file: # Open the file in 'w' (write) mode to clear it.
        writer = csv.writer(file) # Create a CSV writer object for the opened file.
        writer.writerow(headers) # Write the prepared list of headers as the first row.

    print(f"File '{LOG_FILE}' has been initialized with headers.") # Output success message for file setup.

# Function to save a new prediction entry
def log_prediction(features, prediction, confidence, model_version, ground_truth=None): # Define logging function.
    """ # Start of docstring for log_prediction function.
    This function appends a single prediction row to the CSV file. # Summary of method action.
    """ # End of docstring.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Format current time as Year-Month-Day Hour:Min:Sec.

    # Combine all data into a single row list
    row = [timestamp] + features[:5] + [prediction, confidence, model_version, ground_truth] # Merge data parts.
    
    # Append the new row to the end of the existing CSV file
    with open(LOG_FILE, mode='a', newline='') as file: # Open file in 'a' (append) mode to preserve old data.
        writer = csv.writer(file) # Create a CSV writer object for the file stream.
        writer.writerow(row) # Write the new data row to the bottom of the file.
    
    print(f"Prediction logged successfully at {timestamp}") # Print success message with the current time.

# Main entry point for testing the script directly
if __name__ == "__main__": # Check if this script is being run directly by the user.
    initialize_log() # Call the function to setup or reset the CSV file.
    
    test_features = [0.1, 0.2, 0.3, 0.4, 0.5] # Create a list of sample numbers for testing.
    # Log a test prediction with the sample features, a dummy prediction, confidence score, model version, and no ground truth.
    log_prediction(test_features, "Test", 0.99, "v1.0", None) # Execute the log function with test values.
