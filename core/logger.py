import logging

logger = logging.getLogger("travel_wallet")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)
