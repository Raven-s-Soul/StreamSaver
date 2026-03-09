import os
import subprocess
from colorama import just_fix_windows_console
from utils import *

def CoreLogic():
    print_colored("\n=== StreamSaver Tool ===", "cyan")
    
    # --- SETUP INIZIALE ---
    user_input = input(get_colored("Set starting iterator number: ", "red")).strip()
    try:
        start_index = int(user_input)
    except ValueError:
        start_index = 1 
        print_colored("Input non valido. Impostato valore di default: 1", "yellow")
    
    i = start_index
    
    # --- LOOP PRINCIPALE ---
    while True:
        url = input(get_colored("\nEnter a URL or 'exit' to quit: ", "yellow")).strip()
    
        if url.lower() == "exit":
            show_summary(start_index, i)
            break
        if not url:
            continue

        # Verifica durata iniziale
        duration = get_video_duration(url)
        if duration <= 0:
            continue

        output_filename = f"{i}"
        
        # Verifica preventiva esistenza file finale
        skip_merge = os.path.exists(f"{output_filename}.mp4")
        if skip_merge:
            print_colored(f"\n[!] {output_filename}.mp4 esiste già. Scarico solo i pezzi per recupero manuale.", "yellow")
        
        # 1. DOWNLOAD AUDIO
        print_colored(f"[{i}] Downloading Audio...", "white")
        audio_cmd = ['yt-dlp', '--no-warnings', '--quiet', '--progress', '-x', '--audio-format', 'mp3', url, '-o', f'{output_filename}A.mp3']
        if subprocess.run(audio_cmd).returncode != 0:
            continue
        
        # 2. TAGLIO AUDIO (Sincronizzazione)
        audio_raw = f'{output_filename}A.mp3'
        wrong_dur = get_video_duration(audio_raw)
        
        if wrong_dur == -1:
            print_colored("Errore lettura durata audio.", "red")
            continue

        start_diff = max(0, wrong_dur - duration)
        print_colored(f"[{i}] Trimming Audio (Start: {seconds_to_hms(start_diff)})...", "cyan")
        
        trim_cmd = [
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
            '-i', audio_raw,
            '-ss', seconds_to_hms(start_diff),
            '-t', seconds_to_hms(duration), 
            '-c:a', 'copy', f'{output_filename}AF.mp3'
        ]
        
        if subprocess.run(trim_cmd).returncode == 0:
            if os.path.exists(audio_raw): os.remove(audio_raw)
        else:
            continue
        
        # 3. DOWNLOAD VIDEO
        print_colored(f"[{i}] Downloading Video...", "white")
        video_cmd = ['yt-dlp', '--no-warnings', '--quiet', '--progress', '-f', 'bv', url, '-o', f'{output_filename}V.mp4']
        if subprocess.run(video_cmd).returncode != 0:
            continue
        
        # 4. GESTIONE UNIONE O MANUALE
        if skip_merge:
            print_colored(f"[*] {output_filename}.mp4 presente. Parti mantenute: {output_filename}V.mp4 e {output_filename}AF.mp3", "cyan")
            print_colored(f"[*] Comando manuale: ffmpeg -i {output_filename}V.mp4 -i {output_filename}AF.mp3 -c copy {output_filename}_manual.mp4", "purple")
        else:
            # Unione standard
            combine_streams(f'{output_filename}V.mp4', f'{output_filename}AF.mp3', f'{output_filename}.mp4')
        
        i += 1

if __name__ == "__main__":
    just_fix_windows_console()
    missing = check_dependencies()
    if not missing:
        CoreLogic()
    else:
        print_colored("\n[!] ERRORE: Componenti mancanti", "red")
        for tool in missing:
            print_colored(f"  - {tool} non trovato nel PATH", "yellow")
        input("\nPremi Invio per uscire...")