import elasticsearch
from app.models import *
from app.mixin import *

entrys.reindex()
terms.reindex()

print("Added/ refreshed elasticsearch index's")
