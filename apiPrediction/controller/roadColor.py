from flask import Blueprint, request

from interface.service import IService

def getBlueprint(service: IService):
    road_color_blurprint = Blueprint('road_color_blurprint', __name__)

    @road_color_blurprint.route('/road_jf')
    def handle():
        return service.execute()
    return road_color_blurprint
