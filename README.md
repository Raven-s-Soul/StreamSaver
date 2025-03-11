# StreamSaver
>[!NOTE]
>A simple Video downloader using `yt-dlp`, `FFmpeg`.
>
>**No fancy gui** just a single link to paste in a console.
>- *It's not the fastest at all, but works.*

> [!IMPORTANT]
> ## Tampermonkey
> For download with this setup, is needed to have a `url`, you can get it `manualy` or with a `script` using Tampermonkey.
>> Just open [the file](/Video-Manifest-Logger.user.js) and copy all the content into a new script.

> [!TIP]
>### Install Dependencies
>You need to install the [required dependencies](/requirements.txt) as **administrator** (suggested). 
>
>>You can do this by running the following command in your terminal:
>>
>>```bash
>>pip install -r requirements.txt
>>```

> [!CAUTION]
>### Running [StreamSaver.py](/StreamSaver.py)
> The downloads will start with the name of 1.mp4 to x.mp4
>> you can select at start what is the starter number.
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
