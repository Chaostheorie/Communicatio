import elasticsearch
from app.models import *
from app.mixin import *

entrys.reindex()
terms.reindex()
User.reindex()

print("Added/ refreshed elasticsearch index's")
