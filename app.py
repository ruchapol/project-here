from flask import Flask
from service.plus import PlusService
from repository.traffic import TrafficRepo
from controller.traffic_flow import getBlueprint
from controller.health import health_blueprint

app = Flask(__name__)
# Repo
repo = TrafficRepo()
# Service
plusService = PlusService(repo)
# Route
app.register_blueprint(getBlueprint(plusService))
app.register_blueprint(health_blueprint)