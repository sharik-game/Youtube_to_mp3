import moviepy.editor
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s %(asctime)s %(message)s")
def mp3(logger, name: str):
    """
    This function using moviepy to convert mp4 to mp3
    """
    try:
        video = moviepy.editor.VideoFileClip(f"unuseful_cache/{name}.mp4")
        audio = video.audio
        audio.write_audiofile(f"unuseful_cache/{name}.mp3", logger=logger)
        video.close()
        audio.close()
        logging.info("Conversion was successful")
    except Exception as ex:
        logging.error("Some error", exc_info=True)


