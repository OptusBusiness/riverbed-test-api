import requests
import hashlib
import time
import base64
import datetime
import dateutil.parser
import urllib3

urllib3.disable_warnings()


def encode(s):
    return base64.urlsafe_b64encode(s.encode('utf-8'))


def _internal_request(host, url, data=None, headers=None):
    host_part = 'https://{host_id}'
    url_start = host_part.format(host_id=host)
    request_url = "{0}{1}".format(url_start, url)
    r = None
    if data is None:
        # no data is a get request.
        # verify is set to false so SSL errors don't cause problems
        # allow_redirects is false because the NetProfiler REST API
        # uses the location header in a redirect to pass back OAuth2
        # key data.
        r = requests.get(request_url,
                         headers=headers,
                         verify=False,
                         allow_redirects=False)
    else:
        r = requests.post(request_url,
                          data=data,
                          headers=headers,
                          verify=False,
                          allow_redirects=False)
    return r


def get_access_token(host):
    access_key_file = "oauth2.key"

    # The OAuth Token URL
    token_url = '/api/common/1.0/oauth/token'
    with open(access_key_file, 'r') as f:
        file_text = f.readline()
        # strip the text just in case some white space got in there.
        oauth_code = file_text.strip()

    header_encoded = base64.b64encode('{\"alg\":\"none\"}\n'.encode('utf-8')).decode('ascii')

    signature_encoded = ''
    assertion = '.'.join([header_encoded, oauth_code, signature_encoded])
    grant_type = 'access_code'

    state = hashlib.md5((str(time.time())).encode('utf-8')).hexdigest()
    data = {'grant_type': grant_type,
            'assertion': assertion,
            'state': state}

    oauth_sh = _internal_request(host,
                                 token_url,
                                 data=data,
                                 headers={'Accept': 'application/json'})
    oauth_sh_obj = oauth_sh.json()
    oauth_sh_obj['created'] = datetime.datetime.now().isoformat()
    return oauth_sh_obj


def get_authentication_header(host):
    if 'current_access_token' not in globals():
        global current_access_token
        current_access_token = get_access_token(host)
    else:
        created = dateutil.parser.parse(current_access_token['created'])
        expiry_date = created + datetime.timedelta(0, current_access_token['expires_in'])
        if (expiry_date - datetime.datetime.now()).total_seconds() < 0:
            current_access_token = get_access_token(host)

    access_token = current_access_token['access_token']
    return {'Authorization': 'Bearer {0}'.format(access_token),
            'Accept': 'application/json'}


def do_auth_get_request(host, url):
    return _internal_request(host, url, headers=get_authentication_header(host))


def do_auth_post_request(host, url, data):
    return _internal_request(host, url, data=data, headers=get_authentication_header(host))
