from urllib.parse import urljoin

from flask import Blueprint, redirect, request, url_for

from flask_app import oauth_client, repo


bp = Blueprint('authorization', __name__)


@bp.route('/redirect')
def redirect_to_strava():
    full_callback_url = urljoin(request.base_url, 
                                url_for('authorization.handle_callback'))
    external_oauth_url = oauth_client.generate_auth_url(full_callback_url)
    return redirect(external_oauth_url)


@bp.route('/callback')
def handle_callback():
    if (error := request.args.get('error')) is not None:
        # Handles user clicking "cancel" button, resulting in a response like:
        # /callback?state=&error=access_denied
        return {
            'warning': 'It looks like you clicked "cancel" on Strava\'s '
                       'authorization page. If you want to use the Strava API '
                       'to access your data, you must grant access.',
            'error': error
        }

    # Validate that the user accepted the necessary scope,
    # and display a warning if not.
    if 'activity:read_all' not in request.args.get('scope', '').split(','):
        return {
          'warning': 'Please accept the permission '
                    '"View data about your private activities" on Strava\'s '
                    'authorization page (otherwise, you can\'t access your data).',
        }
    
    auth_code = request.args.get('code')

    new_token = oauth_client.exchange_for_token(auth_code)

    repo.save(new_token)

    return new_token.to_dict(), 201
