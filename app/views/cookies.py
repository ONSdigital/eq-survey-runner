from flask import Blueprint, Response

cookies_blueprint = Blueprint('cookies', __name__)

@cookies_blueprint.route('/cookies/accept-all', methods=['GET'])
def set_cookies():

    print('\n\n\n\n\n\n\n\n')
    print('Placeholder just in case I need this')
    print('\n\n\n\n\n\n\n\n')
    return Response(status=404)



