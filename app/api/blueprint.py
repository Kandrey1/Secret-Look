from flask import Blueprint
from flask_restful import Api
from .controllers import AllVoteClient, VoteClient


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(AllVoteClient, '/vote/')
api.add_resource(VoteClient, '/vote/<int:vote_id>')
