import app

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

if __name__ == '__main__':
    app.app.run(debug=True, host="0.0.0.0", port=5000)
