######################################
#       ZEVI BERLIN 12/23/2024       #
#           USER AUTH API            #
#         BACKEND/CONFIG.PY          #
######################################

#==========================================================================#
#======================= TO BE DETERMINED =================================#
#==========================================================================#

######################################
#          INITIALIZATION
#####################
# IMPORT LIBRARIES
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#####################
# CONFIGURE APP
app = Flask(__name__)
CORS(app)
#####################
# CONFIGURE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
######################################

