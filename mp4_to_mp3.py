import moviepy.editor
import logging
def mp3(name: str):
    try:
        video = moviepy.editor.VideoFileClip(f"unuseful_cache/{name}.mp4")
        audio = video.audio
        audio.write_audiofile(f"unuseful_cache/{name}.mp3")
    
    except Exception as ex:
        print(ex)


