from flask import Blueprint, request

from service.plus import PlusService
from repository.traffic import TrafficRepo

from interface.service import IService

def getBlueprint(service: IService):
    traffic_flow_blueprint = Blueprint('traffic_flow_blueprint', __name__)

    @traffic_flow_blueprint.route('/traffic')
    def handle():
        a = request.args.get('a')
        if not a:
            return "Empty argument"
        return service.execute(a)
    return traffic_flow_blueprint
