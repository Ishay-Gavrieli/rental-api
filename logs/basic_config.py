import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(message)s",
                    handlers=[logging.FileHandler("logs/app.log",encoding="utf-8"),
                              logging.StreamHandler()])


logger = logging.getLogger(__name__)




if __name__=="__main__":
    logger.info("start logging")