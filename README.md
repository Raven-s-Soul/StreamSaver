# StreamSaver
>[!NOTE]
>A simple Video downloader using `yt-dlp`, `FFmpeg`.
>
>**No fancy gui** just a single link to paste in a console.
>- *It's not the fastest at all, but works.*

## How to Use
> [!IMPORTANT]
>### 1. [Tampermonkey](https://www.tampermonkey.net/)
>> For download with this setup, is needed to have a `url`, you can get it `manualy` or with a `script` using Tampermonkey.
>>
>>> [Add-on/plug-in](https://www.tampermonkey.net/), then just open [the file](/Video-Manifest-Logger.user.js) and copy all the content into a new tampermonkey script.

> [!TIP]
> ### 2. [FFmpeg](https://www.ffmpeg.org/download.html)
> An open-source tool for converting, editing, and streaming video and audio files in different formats.
>> [Download page](https://www.ffmpeg.org/download.html) or `winget`, `brew`, `apt`, ...

> [!TIP]
>### 3. Install [Python](https://www.python.org/downloads/)
>>Ensure that Python is installed on your system. You can download it from [here](https://www.python.org/downloads/) or `winget`, `brew`, `apt`, ...
>
>### 4. Install Dependencies
>>You need to install the [required dependencies](/requirements.txt) as **administrator** (suggested). 
>>
>>>You can do this by running the following command in your terminal:
>>>
>>>```bash
>>>pip install -r requirements.txt
>>>```

> [!CAUTION]
>### 5. Running [StreamSaver.py](/StreamSaver.py)
> The downloads will start with the name of 1.mp4 to x.mp4
>> you can select at start what is the starter number.

> [!WARNING]
> Do not download more than 3 request at the same time, you may risk get ip banned or else.
>- Suggest to wait a little when downloading in big chunks.
***
## Alternatives (Those are prone to audio errors)
>Single console command: 
>```python
>yt-dlp <url> -o <filename.mp4>
>```

>Script: 
>```python
>import os
>
>i = 1
>while True:
>    user_input = input("Enter a URL or 'exit' to quit: ")
>    
>    if user_input.lower() == "exit":
>        print("Exiting the loop.")
>        break
>
>    output_filename = f"{i}.mp4"  # Format the output filename dynamically with 'i'
>    
>    # Run yt-dlp with the given URL and output filename
>    s = os.system(f'yt-dlp "{user_input}" -o "{output_filename}"')
>    if(s == 0)
>        i += 1
>```
