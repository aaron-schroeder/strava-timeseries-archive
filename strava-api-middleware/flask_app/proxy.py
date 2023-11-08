from flask import Blueprint, request

from flask_app import commands
from flask_app import repo, rate_limit
from oauth.domain.model import ResourceHttpClient


bp = Blueprint('proxy', __name__, url_prefix='/proxy')


@bp.route('/<path:resource_relative_url>', methods=['GET'])
def handle_proxy_request(resource_relative_url):
    # # return commands.make_authenticated_get_request(resource_relative_url)
    # # token = oauth_client.exchange_for_token(code)
    # token = oauth_client.refresh(token)
    # # rsrc_http_client = AuthenticatedHttpClient(bearer_token)
    # rsrc_http_client = AuthenticatedHttpClient()
    # # rsrc_http_client.set_token(bearer_token)
    # resp = rsrc_http_client.get(resource_relative_url)

    # Check stored rate limit
    if rate_limit.is_active:
        rate_limit_msg = {
            'message': 'Resource server rate limit in effect. Try again after '
                       + rate_limit.lifts_at.strftime('%H:%M:%S UTC')
        }
        return rate_limit_msg, 429
    
    access_token = commands.get_fresh_token(repo)

    if access_token is None:
        return {'message': 'Do the handshake first.'}, 401

    resource_client = ResourceHttpClient(access_token)

    response = resource_client.get(
        'https://www.strava.com/api/v3/' + resource_relative_url,
        params=request.args
    )

    rate_limit.update_from(response)

    if response.status_code == 429:
        err_msg = 'Rate limited. Aborting for now. Try again at the next :15'
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
