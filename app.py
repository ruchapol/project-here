from flask import Flask
from api.service.plus import PlusService
from repository.traffic import TrafficRepo
from api.controller.traffic_flow import getBlueprint
from api.controller.health import health_blueprint

app = Flask(__name__)
# Repo
repo = TrafficRepo()
# Service
plusService = PlusService(repo)
# Route
app.register_blueprint(getBlueprint(plusService))
app.register_blueprint(health_blueprint)