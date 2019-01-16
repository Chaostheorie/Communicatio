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
#   License in LICENSE    #
###########################

###########################
#      Version 0.0.1      #
###########################
"""
print(info)

app.run(debug=True, host="0.0.0.0", port=5000)
