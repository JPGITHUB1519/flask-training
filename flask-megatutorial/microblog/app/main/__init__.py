from flask import Blueprint
from ..models import Permission

main = Blueprint('main', __name__)

# avoiding circular dependecies
from . import views, errors


# Permission global variable to all main templates
@main.app_context_processor
def inject_permissions():
	return dict(Permission=Permission)