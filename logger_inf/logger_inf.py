import logging

logging.basicConfig(
    level=logging.WARNING,
    filename="log.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
)

logger = logging.getLogger(__name__)