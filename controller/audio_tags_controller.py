from flask import request, g
from flask_restful import Resource

from interceptor.interceptor import login_required
from service.audio_tags_service import AudioTagsService
from utils.response import Response


class AudioTagsController(Resource):
    @login_required
    def post(self):
        tag_name = request.args.get("tag_name")
        if not tag_name or '' == tag_name:
            return Response.error('标签名不能为空')
        return AudioTagsService.add_audio_tags(g.username, tag_name)

    @login_required
    def get(self):
        return AudioTagsService.query_audio_tags(g.username)

    @login_required
    def delete(self):
        tag_name = request.args.get("tag_name")
        if not tag_name or '' == tag_name:
            return Response.error('标签名不能为空')
        return AudioTagsService.delete_audio_tags(g.username, tag_name)
