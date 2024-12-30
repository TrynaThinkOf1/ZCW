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
from flask_session import Session

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
# CONFIGURE SESSIONS
app.config['SECRET_KEY'] = os.environ['user_auth_api_FLASK_SESSION_TOKEN']
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'flask_session:'

session_file_dir = os.path.join(os.getcwd(), '.flask_session')
os.makedirs(session_file_dir, exist_ok=True)
app.config['SESSION_FILE_DIR'] = session_file_dir

Session(app)

print(f"SESSION_TYPE: {app.config.get('SESSION_TYPE')}")
######################################

banner_text = """
ZEVI BERLIN
--------------------
Starting up...
User Auth API Ready
"""
console.print(Panel(banner_text, expand=False, border_style="bright_cyan"))

