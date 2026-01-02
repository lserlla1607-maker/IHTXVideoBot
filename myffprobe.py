import subprocess
import json
def FFprobe(file_path:str):
    """
    Runs ffprobe on a file and returns the output as a Python dictionary.
    """
    command_array = [
        "ffprobe", 
        "-v", "quiet",  # Suppress logging to stderr
        "-print_format", "json",  # Output in JSON format
        "-show_format",  # Show format information
        "-show_streams",  # Show stream information
        str(file_path)  # File path
    ]

    try:
        result = subprocess.run(
            command_array, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,  # For Python 3.7+; use universal_newlines=True for older versions
            check=True  # Raise CalledProcessError if the command fails
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: ffprobe command not found. Make sure it's installed and in your PATH.")
        return None