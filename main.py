import os
import subprocess
import signal
import time

livestream_url = "http://example.com/livestream"  # Replace with the actual audio livestream source URL
output_directory = "/your/archive"  # Directory where the archived MP3 files will be saved
conversion_command = ["ffmpeg", "-i", "", "-c:a", "libmp3lame", "-b:a", "128k", ""]

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

def convert_to_mp3(input_file, output_file):
    conversion_command[2] = input_file
    conversion_command[5] = output_file

    subprocess.run(conversion_command)

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
output_file = os.path.join(output_directory, f"archive_{current_timestamp}.mp3")

# Start recording the livestream
ffmpeg_command = ["ffmpeg", "-i", livestream_url, "-c:a", "copy", "-t", str(archiving_duration), output_file]
process = subprocess.Popen(ffmpeg_command, preexec_fn=os.setsid)

# Wait for the archiving process to complete or be interrupted
process.wait()

# Convert the recorded file to MP3 format
convert_to_mp3(output_file, output_file[:-4] + ".mp3")
print("Archived:", output_file[:-4] + ".mp3")

# Optionally, you can delete the original recorded file after archiving
# os.remove(output_file)