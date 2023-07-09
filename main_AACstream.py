import os
import subprocess
import signal
import time

livestream_url = "http://example.com/livestream"  # Replace with the actual audio livestream source URL
output_directory = "/your/archive"  # Directory where the archived AAC files will be saved
radioname = ""  # Radiostream name (or any name of the archive)

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Signal handler for interrupting the archiving process
def signal_handler(signal, frame):
    print("\nArchiving process interrupted.")
    # Perform any cleanup or finalization tasks if needed
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Archiving duration (in seconds)
archiving_duration = 60 * 60 * 24  # 24 hours

# Generate output file path
current_timestamp = time.strftime("%Y%m%d-%H%M%S")
output_file = os.path.join(output_directory, f"{radioname}_archive_{current_timestamp}.aac")

# Start recording the livestream to an AAC file
ffmpeg_command = ["ffmpeg", "-i", livestream_url, "-c:a", "aac", "-t", str(archiving_duration), output_file]
process = subprocess.Popen(ffmpeg_command, preexec_fn=os.setsid)

# Wait for the archiving process to complete or be interrupted
process.wait()

print("Archived:", output_file)
