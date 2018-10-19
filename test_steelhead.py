import oauth2_request
import json
import datetime
import argparse


def print_request(url, data=''):
    if data == '':
        response = oauth2_request.do_auth_get_request(host, url)
    else:
        response = oauth2_request.do_auth_post_request(host, url, data)
    print('URL: {0}'.format(url))
    print('Response:')
    print(json.dumps(response.json(), sort_keys=False, indent=6))
    print('\n\n')


def datetime_since_epoch(date: datetime):
    ep = datetime.datetime(1970, 1, 1, 0, 0, 0)
    x = (date - ep).total_seconds()
    return x


def main():
    global host
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="hostname or ip address of SteelHead device")
    parser.add_argument("--device_id", help="device_id of SteelHead device for query criteria")
    parser.add_argument("--interval", help="interval between start_time and end_time for "
                                           "Riverbed REST API ")
    parser.add_argument("--keyfile", help='Filename with the OAUTH key')
    args = parser.parse_args()
    host = args.host
    device_id = args.device_id

    if args.keyfile:
        oauth2_request.set_request_keyfile(args.keyfile)

    print_request('/api/sh.appflow/2.0/networks')
    print_request('/api/sh.appflow/2.0/applications')
    print_request('/api/sh.appflow/2.0/sites')
    print_request('/api/sh.appflow/2.0/qos_profiles')


if __name__ == "__main__":
    # execute only if run as a script
    main()
