import moviepy.editor
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s %(asctime)s %(message)s")
def mp3(name: str):
    try:
        video = moviepy.editor.VideoFileClip(f"unuseful_cache/{name}.mp4")
        audio = video.audio
        audio.write_audiofile(f"unuseful_cache/{name}.mp3")
        logging.info("conversion was successful")
    except Exception as ex:
        logging.error("Some error", exc_info=True)


