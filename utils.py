import subprocess
import os

def get_colored(text, color):
    """Restituisce una stringa formattata con codici colore ANSI."""
    colors = {
        'red': '\033[31m', 'green': '\033[32m', 'yellow': '\033[33m',
        'blue': '\033[34m', 'purple': '\033[35m', 'cyan': '\033[36m',
        'white': '\033[37m', 'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"


def print_colored(text, color):
    """Stampa testo colorato nel terminale."""
    print(get_colored(text, color))


def check_dependencies():
    """Verifica se i tool esterni sono installati nel sistema."""
    tools = ['ffmpeg', 'ffprobe', 'yt-dlp']
    missing = []
    for tool in tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=False)
        except FileNotFoundError:
            missing.append(tool)
    return missing


def seconds_to_hms(seconds):
    """Converte i secondi nel formato HH:MM:SS."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def get_video_duration(user_input):
    """Recupera la durata di un video tramite ffprobe."""
    command = [
        'ffprobe', '-i', user_input, 
        '-show_entries', 'format=duration',
        '-v', 'quiet', '-of', 'csv=p=0'
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        return -1
    return round(float(result.stdout.strip()))


def combine_streams(video_path, audio_path, output_path):
    """Unisce i flussi e conferma il successo fisico sul disco."""
    try:
        subprocess.run([
            'ffmpeg', '-n',
            '-i', video_path, 
            '-i', audio_path,
            '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
            output_path
        ], check=True) 

        # Doppio check: il file esiste ed è utilizzabile?
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print_colored(f"\n[OK] Unione completata con successo: {output_path}", "green")
            if os.path.exists(video_path): os.remove(video_path)
            if os.path.exists(audio_path): os.remove(audio_path)
            return True
        else:
            raise Exception("File prodotto vuoto o mancante.")

    except (subprocess.CalledProcessError, Exception) as e:
        print_colored(f"\n[!] ERRORE CRITICO NELL'UNIONE: {e}", "red")
        print_colored("I file temporanei (V e AF) sono stati MANTENUTI.", "yellow")
        return False


def show_summary(start, current):
    """Mostra il report finale della sessione."""
    total = current - start
    print_colored("\n" + "="*35, "cyan")
    if total > 0:
        print_colored("  SESSIONE COMPLETATA", "green")
        print_colored(f"  Video salvati: {total}", "white")
        print_colored(f"  Indici: da {start} a {current-1}", "white")
    else:
        print_colored("  Sessione chiusa - Nessun file", "yellow")
    print_colored("="*35 + "\n", "cyan")