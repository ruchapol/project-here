from flask import Blueprint, request

from interface.service import IService

def getBlueprint(service: IService):
    predict_travel_time_blurprint = Blueprint('predict_travel_time_blurprint', __name__)

    @predict_travel_time_blurprint.route('/travel_time')
    def handle():
        destination = request.args.get('destination')
        time = request.args.get('time')
        if not destination or not time:
            return "Empty argument"
        return service.execute(destination, time)
    return predict_travel_time_blurprint
