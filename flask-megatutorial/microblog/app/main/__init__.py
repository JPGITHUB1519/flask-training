from flask import Blueprint

main = Blueprint('main', __name__)

# avoiding circular dependecies
from . import views, errors