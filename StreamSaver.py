import os
import subprocess
import shutil
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
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def combine_streams(video_path, audio_path, output_path):
    # Controlla se ffmpeg è disponibile
    if shutil.which('ffmpeg') is None:
        print_colored("Errore: ffmpeg non è installato o non è nel PATH.", "red")
        return

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
        print_colored("FFmpeg non è riuscito a combinare audio e video. Assicurati che sia installato correttamente.", "red")
    finally:
        # Usa try/except per evitare errori se i file non esistono
        try:
            os.remove(video_path)
        except Exception:
            pass
        try:
            os.remove(audio_path)
        except Exception:
            pass

def get_video_duration(user_input):
    # Verifica che ffprobe sia disponibile
    if shutil.which('ffprobe') is None:
        print_colored("Errore: ffprobe non è installato o non è nel PATH. Installa ffmpeg per ottenere ffprobe.", "red")
        return -1

    command = [
        'ffprobe', '-i', user_input, 
        '-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=p=0'
    ]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError as e:
        print_colored(f"Errore: {e}. Assicurati che ffprobe sia installato e nel PATH.", "red")
        return -1
    
    if result.returncode != 0:
        print_colored("Errore: Impossibile ottenere la durata del video.", "red")
        print_colored(result.stderr, "red")
        return -1

    try:
        duration = round(float(result.stdout.strip()))
    except ValueError:
        print_colored("Errore: Impossibile interpretare la durata del video.", "red")
        return -1

    return duration
    
def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def CoreLogic():
    print_colored("Set starting iterator number", "red")
    user_input = input()
    try:
        i = int(user_input)
    except ValueError:
        i = 1  # Default to 1 if input is invalid
    
    while True:
        print_colored("Enter a URL or 'exit' to quit: ", "yellow")
        user_input = input()
    
        if user_input.lower() == "exit":
            print_colored("Exiting the loop.", "yellow")
            break

        output_filename = f"{i}"
        duration = get_video_duration(user_input)
        if duration == -1:
            continue
            
        # Estrae l'audio con yt-dlp
        a = os.system(f'yt-dlp -x --audio-format mp3 "{user_input}" -o "{output_filename}A.mp3"')
        if a != 0:
            continue
        print_colored("Audio estratto", "yellow")
        
        # Controlla la durata dell'audio estratto
        wrong_duration = get_video_duration(f'{output_filename}A.mp3')
        if wrong_duration == -1:
            continue

        # Usa ffmpeg per tagliare l'audio
        start_time = seconds_to_hms(wrong_duration - duration)
        s = os.system(f'ffmpeg -i {output_filename}A.mp3 -ss {start_time} -t {seconds_to_hms(wrong_duration)} -c copy {output_filename}AF.mp3')
        if s != 0:
            continue
        try:
            os.remove(f'{output_filename}A.mp3')
        except Exception:
            pass
        print_colored("Audio tagliato", "cyan")
        
        # Estrae il video con yt-dlp
        v = os.system(f'yt-dlp -f bv "{user_input}" -o "{output_filename}V.mp4"')
        if v != 0:
            continue
        print_colored("Video estratto", "yellow")
        
        # Combina video e audio
        combine_streams(f'{output_filename}V.mp4', f'{output_filename}AF.mp3', f'{output_filename}.mp4')
        
        i += 1
        
if __name__ == "__main__":
    just_fix_windows_console()  # È sicuro chiamare questa funzione anche su piattaforme non-Windows
    CoreLogic()
