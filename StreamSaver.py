import os
import subprocess
from colorama import just_fix_windows_console

def print_colored(text, color):
    colors = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'  # Reset to default color
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

#Combines video and audio streams using FFmpeg
def combine_streams(video_path, audio_path, output_path):
    try:
        subprocess.run(
            [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-strict', 'experimental',
                output_path
            ],
            check=True
        )
        print_colored(f"Combined video saved: {output_path}", "green")
    except subprocess.CalledProcessError:
        print_colored("FFmpeg failed to combine audio and video. Please ensure it is installed.", "red")
    finally:
        print("Done")
        os.remove(video_path)
        os.remove(audio_path)

def get_video_duration(user_input):
    # ffprobe -i "video_url_or_file" -show_entries format=duration -v quiet -of csv="p=0
    command = [
        'ffprobe', '-i', user_input, 
        '-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=p=0'  
    ]
    
    # Run the command and capture the output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Check if there's an error
    if result.returncode != 0:
        print_colored("Error: Unable to get video duration.", "red")
        print_colored(result.stderr, "red")  # Print any error message
        return -1

    # Parse the duration from the output
    return round(float(result.stdout.strip()))
    
def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def CoreLogic():
    #Iter
    print_colored("Set starting iterator number", "red")
    user_input = input()
    try:
        i = int(user_input)
    except ValueError:
        i = 1  # Default to 1 if the input is invalid
    
    lista = []
    
    while True:
        print_colored("add to a list or 'exit'", "green")
        user_input = input()
        
        if "http" in user_input:
            lista.append(user_input.strip()) # cleaned input
        
        if user_input.lower() == "exit":
            print_colored("Exiting the loop.", "yellow")
            break    
    
    while True:
        if not lista:
            print_colored("Enter a URL or 'exit' to quit: ", "yellow")
            user_input = input()
        else:
            user_input = lista.pop(0)
    
        if user_input.lower() == "exit":
            print_colored("Exiting the loop.", "yellow")
            break

        output_filename = f"{i}"
        duration = get_video_duration(user_input)
        if duration == -1 and lista:
            i += 1
            print_colored("Error found, skip", "cyan")
            continue
        if duration == -1:
            continue
            
        # yt-dlp -x --audio-format mp3 "" -o output.mp3
        a = os.system(f'yt-dlp -x --audio-format mp3 "{user_input}" -o "{output_filename}A.mp3"')
        if a != 0:
            continue
        print_colored("Audio", "yellow")
        
        # strip audio to last duration
        WrongDuration = get_video_duration(f'{output_filename}A.mp3')
        if WrongDuration == -1:
            continue

        # ffmpeg -i input_audio.mp3 -ss 00:01:30 -t 00:02:00 -c copy output_audio.mp3
        s = os.system(f'ffmpeg -i {output_filename}A.mp3 -ss {seconds_to_hms(WrongDuration-duration)} -t {seconds_to_hms(WrongDuration)} -c copy {output_filename}AF.mp3')
        if s != 0:
            continue
        os.remove(f'{output_filename}A.mp3')
        print_colored("Cut Audio", "cyan")
        
        # yt-dlp -f bv "input" -o outputvideo.mp4 
        v = os.system(f'yt-dlp -f bv "{user_input}" -o "{output_filename}V.mp4"')
        if v != 0:
            continue
        print_colored("Video", "yellow")
        
        # combine ffmpeg     
        combine_streams(f'{output_filename}V.mp4',f'{output_filename}AF.mp3',f'{output_filename}.mp4')
        
        i += 1
        
    
if __name__ == "__main__":
    just_fix_windows_console() #it’s safe to call this function on non-Windows platforms
    CoreLogic()
