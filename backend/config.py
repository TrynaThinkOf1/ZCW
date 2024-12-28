###################################
# user-auth-api/backend/config.py #
###################################

#==========================================================================#
#============================ CONFIGURATION ===============================#
#==========================================================================#

######################################
#          INITIALIZATION
#####################
# IMPORT LIBRARIES
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import os
from datetime import timedelta

from rich.console import Console
from rich.panel import Panel
#####################
# CONFIGURE APP
app = Flask(__name__)
CORS(app)

console = Console()
#####################
# CONFIGURE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#####################
# CONFIGURE JWT
app.config['JWT_SECRET_KEY'] = os.environ['user_auth_api_FLASK_JWT_TOKEN']
app.config['JWT_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)
######################################

banner_text = """
ZEVI BERLIN
--------------------
Starting up...
User Auth API Ready
"""
console.print(Panel(banner_text, expand=False, border_style="bright_cyan"))

