def navigate_to_page(client, page):
    resp = client.get(page, follow_redirects=False)
    if resp.status_code != 200:
        raise RuntimeError('Expected 200 response but got {code}'.format(code=resp.status_code))
    return resp
