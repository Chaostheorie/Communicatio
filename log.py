import logging

# for potentially loggign sql changes to log file
handler = logging.FileHandler('app.log')
handler.setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy').addHandler(handler)
