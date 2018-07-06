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
    parser.add_argument("host", help="hostname or ip address")
    parser.add_argument("--device_id", help="device_id for query criteria")
    args = parser.parse_args()
    host = args.host
    device_id = args.device_id

    datetime_criteria = {
        "start_time": datetime_since_epoch(datetime.datetime.now() - datetime.timedelta(3)),
        "end_time": datetime_since_epoch(datetime.datetime.now()),
    }

    multiple_devices_criteria = dict(datetime_criteria)
    multiple_devices_criteria['devices'] = [device_id]

    print_request('/api/cmc.topology/1.2/bandwidth_usage')
    print_request('/api/cmc.stats/1.0/disk_load', json.dumps(datetime_criteria))

    connection_query_stats = dict(datetime_criteria)
    connection_query_stats['device'] = device_id
    print_request('/api/cmc.stats/1.0/connection_history', json.dumps(connection_query_stats))

    print_request('/api/cmc.stats/1.0/connection_forwarding', json.dumps(multiple_devices_criteria))
    print_request('/api/cmc.stats/1.0/connection_pooling', json.dumps(multiple_devices_criteria))
    qos1_query_criteria = dict(connection_query_stats)
    qos1_query_criteria['traffic_type'] = 'inbound'
    print_request('/api/cmc.stats/1.0/qos', json.dumps(qos1_query_criteria))
    qos2_query_criteria = dict(connection_query_stats)
    qos2_query_criteria['traffic_type'] = 'outbound'
    print_request('/api/cmc.stats/1.0/qos', json.dumps(qos2_query_criteria))

    print_request('/api/cmc.stats/1.0/throughput', json.dumps(connection_query_stats))

    print_request('/api/cmc.stats/1.0/bandwidth/usage', json.dumps(multiple_devices_criteria))
    print_request('/api/cmc.stats/1.0/bandwidth/timeseries', json.dumps(multiple_devices_criteria))
    print_request('/api/cmc.stats/1.0/bandwidth/per_appliance', json.dumps(multiple_devices_criteria))
    print_request('/api/cmc.stats/1.0/dns/cache_hits', json.dumps(multiple_devices_criteria))
    print_request('/api/cmc.stats/1.0/dns/usage', json.dumps(multiple_devices_criteria))
    print_request('/api/cmc.stats/1.0/http', json.dumps(multiple_devices_criteria))
    print_request('/api/cmc.stats/1.0/nfs', json.dumps(multiple_devices_criteria))
    print_request('/api/cmc.stats/1.0/srdf', json.dumps(connection_query_stats))
    print_request('/api/cmc.stats/1.0/ssl', json.dumps(connection_query_stats))
    print_request('/api/cmc.stats/1.0/pfs', json.dumps(connection_query_stats))
    print_request('/api/cmc.web-proxy/2.0/profiles')

    print_request('/api/cmc.stats/1.0/granite/lun_io', json.dumps(connection_query_stats))
    print_request('/api/cmc.stats/1.0/granite/initiator_io', json.dumps(connection_query_stats))
    print_request('/api/cmc.stats/1.0/granite/network_io', json.dumps(connection_query_stats))


if __name__ == "__main__":
    # execute only if run as a script
    main()


