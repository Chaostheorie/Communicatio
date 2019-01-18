import elasticsearch
from app.models import entrys, terms

# Add/ refresh indexes for elasticsearch and make the search working
entrys.reindex()
terms.reindex()

from app import app

info = """
###########################
#     VKS-Development     #
#     by Chasotheorie     #
###########################

###########################
#    Development build    #
#       Do Not use        #
# in prduction enviroment #
###########################

###########################
#     Licensed under      #
#     GNU GENERAL         #
#     PUBLIC LICENSE      #
###########################

###########################
#      Version 0.0.1      #
###########################
"""
print(info)

app.run(debug=True, host="0.0.0.0", port=5000)
