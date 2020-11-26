import json


def analytics_allowed(request):
    cookie_policy = request.cookies.get('ons_cookie_policy')

    if cookie_policy:
        return json.loads(cookie_policy.replace("'", "\""))["usage"]
    else:
        return False
