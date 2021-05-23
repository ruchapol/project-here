from flask import Blueprint

health_blueprint = Blueprint('health', __name__)

@health_blueprint.route('/health')
def index():
    return "I'm healthy !"