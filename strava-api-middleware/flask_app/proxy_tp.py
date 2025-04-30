import os

from flask import Blueprint, request

from flask_app import commands
from flask_app import tp_oauth_client, tp_repo # , repo, rate_limit
from oauth.domain.model import ResourceHttpClient


bp = Blueprint('proxy-tp', __name__, url_prefix='/proxy-tp')


@bp.route('/<path:resource_relative_url>', methods=['GET'])
def handle_proxy_request(resource_relative_url):

    # This command assumes there is already a token in the repo,
    # and does not handle the initial get of the token from TP
    # nor the save.
    access_token = commands.get_fresh_tp_token(tp_repo, tp_oauth_client)
    
    # access_token = tp_oauth_client.get_token()

    # return {'token': access_token}, 401  # DEBUG

    if access_token is None:
        return {'message': 'Configure TP settings first.'}, 401

    resource_client = ResourceHttpClient(access_token)

    response = resource_client.get(
        'https://tpapi.trainingpeaks.com/' + resource_relative_url,
        params=request.args
    )

    if response.status_code == 429:
        err_msg = 'Maybe rate-limited? Aborting for now.'
        return {'error': err_msg}, 429
    elif response.status_code == 401:
        print(response.text)
        return {'error': 'API says unauthorized.'}, 401
    elif response.status_code == 403:
        print(response.text)
        return {'error': 'API says resource is forbidden.'}, 403
    elif response.status_code == 404:
        print(response.text)
        return {'error': 'No resource found.'}, 404

    return response.json(), 200
