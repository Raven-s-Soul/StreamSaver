# StreamSaver

> **NOTE:**  
> A simple video downloader using `yt-dlp` and `FFmpeg`.  
> **No fancy GUI:** Just paste a single link into the console.  
> *It's not the fastest solution, but it works.*

---

> **IMPORTANT: Tampermonkey**  
> For downloads with this setup, you need a valid URL. You can obtain the URL manually or by using a script with Tampermonkey.  
>  
> To use Tampermonkey:  
> 1. Open [Video-Manifest-Logger.user.js](/Video-Manifest-Logger.user.js).  
> 2. Copy all the content into a new Tampermonkey script.

---

> **TIP: Install Dependencies**  
> You need to install the [required dependencies](/requirements.txt) with **administrator** privileges (recommended).  
>
> Run the following command in your terminal:  
> ```bash
> pip install -r requirements.txt
> ```

---

> **CAUTION: Running [StreamSaver.py](/StreamSaver.py)**  
> The downloads will be named sequentially from `1.mp4` to `x.mp4`.  
> You can select the starting number at the beginning of the script.

---

> **WARNING:**  
> Do not download more than 3 requests at the same time. Downloading in big chunks may result in your IP being banned or other issues.  
> *It is suggested to wait a little between large downloads.*

---

## Alternatives  
*(Note: These alternatives are prone to audio errors)*

### Single Console Command
```python
yt-dlp <url> -o <filename.mp4>


import os

i = 1
while True:
    user_input = input("Enter a URL or 'exit' to quit: ")
    
    if user_input.lower() == "exit":
        print("Exiting the loop.")
        break

    output_filename = f"{i}.mp4"  # Format the output filename dynamically with 'i'
    
    # Run yt-dlp with the given URL and output filename
    s = os.system(f'yt-dlp "{user_input}" -o "{output_filename}"')
    if s == 0:
        i += 1
