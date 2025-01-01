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
from itsdangerous import URLSafeTimedSerializer

import os
from datetime import timedelta

from rich.console import Console
from rich.panel import Panel
#####################
# CONFIGURE APP
app = Flask(__name__)
CORS(app, supports_credentials=True)

console = Console()
#####################
# CONFIGURE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
#####################
# CONFIGURE SESSIONS
app.secret_key = os.environ.get("user_auth_api_FLASK_SESSION_TOKEN")
serializer = URLSafeTimedSerializer(app.secret_key)
######################################

banner_text = """
ZEVI BERLIN
--------------------
Starting up...
User Auth API Ready
"""
console.print(Panel(banner_text, expand=False, border_style="bright_cyan"))

