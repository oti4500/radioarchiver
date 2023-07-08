import os
import subprocess
import signal
import time

livestream_url = "http://example.com/livestream"  # Replace with the actual audio livestream source URL
output_directory = "/your/archive"  # Directory where the archived Vorbis files will be saved
conversion_command = ["ffmpeg", "-i", "", "-c:a", "libvorbis", "-q:a", "5", ""]

radioname = ""  # Radiostream name (or any name of the archive)

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)


def convert_to_vorbis(input_file, output_file):
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
output_file = os.path.join(output_directory, f"{radioname}_archive_{current_timestamp}.ogg")

# Start recording the livestream
ffmpeg_command = ["ffmpeg", "-i", livestream_url, "-c:a", "copy", "-t", str(archiving_duration), output_file]
process = subprocess.Popen(ffmpeg_command, preexec_fn=os.setsid)

# Wait for the archiving process to complete or be interrupted
process.wait()

# Convert the recorded file to Vorbis format
convert_to_vorbis(output_file, output_file[:-4] + ".ogg")
print("Archived:", output_file[:-4] + ".ogg")

# Optionally, you can delete the original recorded file after archiving
# os.remove(output_file)
