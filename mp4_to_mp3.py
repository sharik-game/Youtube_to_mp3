import logging
import moviepy.editor 
from proglog.proglog import ProgressBarLogger
from db import Redis_endpoints
logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s %(asctime)s %(message)s")
class MyBarLogger(ProgressBarLogger):
    def callback(self, **changes):
        # Every time the logger message is updated, this function is called with
        # the `changes` dictionary of the form `parameter: new value`.
        for (parameter, value) in changes.items():
            print('Parameter %s is now %s' % (parameter, value))
    def bars_callback(self, bar, attr, value, old_value=None):
        # Every time the logger progress is updated, this function is called        
        percentage = (value / self.bars[bar]['total']) * 100
        # print(int(percentage))

logger = MyBarLogger()
def mp3(db: Redis_endpoints, token: str, name: str):
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
        logging.warning("Redis begin")
        db.set_value("token", token)
        logging.info(db.get_value("token"))
        db.set_value("token", token + " test")
        logging.info(db.get_value("token"))
        logging.warning("Redis end")
    except Exception as ex:
        logging.error("Some error", exc_info=True)


