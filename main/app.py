from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from main.config import Configuration


# Initialize Flask app
app = Flask(__name__)


# Set app configurations
app.config.from_object(Configuration)


# Initialize email client, it will be used to send emails to users
# When confirming their accounts
mail = Mail()
mail.init_app(app)


# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Set ( migrate ) shell commands
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
