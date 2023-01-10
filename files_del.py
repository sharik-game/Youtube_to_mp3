# import shutil
import logging
import os
logging.basicConfig(level=logging.INFO, format="%(levelname)s:   %(name)s %(asctime)s %(message)s")
def delete_file():
    try:
        my_dir = "unuseful_cache"
        for files in os.listdir(my_dir):
            os.remove(os.path.join(my_dir, files))
        # shutil.rmtree(f"unuseful_cache")
        # os.mkdir(f"unuseful_cache")
        logging.warning("deleting was succesful")
    except Exception as ex:
        logging.error("ERROR", exc_info=True)