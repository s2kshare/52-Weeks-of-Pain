import os
from datetime import datetime  # Fixing the import

class ErrorHandler:
    def __init__(self, title="No Title", message="No Message", log_file="error_log.txt"):
        self.errMessage = message
        self.errTitle = title
        self.log_file = log_file

    def log_error(self):
        # Print to console
        print(f"[ERROR]: {self.errTitle}\n[ERR_MSG]: {self.errMessage}")
        self.log_to_file()
    
    def set_error_title(self, title):
        self.errTitle = title

    def set_error_message(self, message):
        self.errMessage = message

    def clear_error(self):
        self.errMessage = "No Message"

    def log_to_file(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Creation of error log file
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("Error Log\n")
                f.write("="*40 + "\n")

        # Append the error message to log file
        with open(self.log_file, 'a') as f:  # Changed self.log_error to self.log_file
            f.write(f"<{timestamp}>\n")
            f.write(f"[ERROR]: {self.errTitle}\n")
            f.write(f"[ERR_MSG]: {self.errMessage}\n")
            f.write("-"*40 + "\n")  # Separator for readability
