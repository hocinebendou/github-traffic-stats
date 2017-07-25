#!/usr/bin/env python

import argparse
import csv, os
from collections import OrderedDict
import datetime
import getpass
import requests

# Globals
current_timestamp = str(datetime.datetime.now().strftime('%Y-%m-%d-%Hh-%Mm'))  # was .strftime('%Y-%m-%d'))
path = os.path.dirname(os.path.abspath(__file__))
top_dir = os.path.split(path)[0]
csv_views = top_dir + '/git-traffics/data/' + current_timestamp + '-traffic-stats-views.csv'
csv_clones = top_dir + '/git-traffics/data/' + current_timestamp + '-traffic-stats-clones.csv'


def send_request(resource, auth, repo=None, op='clones', headers=None):
    """Send request to Github API
    :param resource: string - specify the API to call
    :param auth: tuple - username-password tuple
    :param repo: string - if specified, the specific repository name
    :param headers: dict - if specified, the request headers
    :return: response - GET request response
    """
    if resource == 'traffic':
        base_url = 'https://api.github.com/repos/'
        base_url = base_url + auth[0] + '/' + repo + '/traffic/' + op
        response = requests.get(base_url, auth=auth, headers=headers)
        return response
    else:
        return None


def json_to_table(repo, json_response, op='clones'):
    """
        Parse traffic stats in JSON and format into a table
        :param repo: str - the GitHub repository name
        :param json_response: json - the json input
        :return: table: str - for printing on command line
    """
    repo_name = repo
    total_op = str(json_response['count'])
    total_uniques = str(json_response['uniques'])

    dates_and_op = OrderedDict()
    detailed_op = json_response[op]
    for row in detailed_op:
        utc_date = str(row['timestamp'][0:10])
        dates_and_op[utc_date] = (str(row['count']), str(row['uniques']))

    """Table template
    repo_name
    Date        Op   Unique visitors
    Totals      #       #
    date        #       #
    ...         ...     ...
    """
    operation = 'Clones' if op == 'clones' else 'Views'
    table_alt = repo_name + '\n' + \
                '# Total ' + operation + ':' + '\t' + total_op + '\n' + '# Total Unique:' + '\t' + total_uniques + '\n' + \
                'Date' + '\t\t' + operation + '\t' + 'Unique visitors' + '\n'

    table = repo_name + '\n' + \
            'Date' + '\t\t' + operation + '\t' + 'Unique visitors' + '\n' + \
            'Totals' + '\t\t' + total_op + '\t' + total_uniques + '\n'
    for row in dates_and_op:
        table += row + '\t' + dates_and_op[row][0] + '\t' + dates_and_op[row][1] + '\n'

    return table


def store_csv(repo, json_response, csv_file_name, op='clones'):
    """Store the traffic stats as a CSV, with schema:
    repo_name, date, clones, unique_visitors

    :param repo: str - the GitHub repository name
    :param json_response: json - the json input
    :return:
    """
    repo_name = repo

    dates_and_op = OrderedDict()
    detailed_op = json_response[op]
    for row in detailed_op:
        utc_date = str(row['timestamp'][0:10])
        dates_and_op[utc_date] = (str(row['count']), str(row['uniques']))

    # Starting up the CSV, writing the headers in a first pass
    # Check if existing CSV
    try:
        csv_file = open(csv_file_name).readlines()
        if csv_file:
            for i in dates_and_op:
                row = [repo_name, i, dates_and_op[i][0], dates_and_op[i][1]]
                with open(csv_file_name, 'a') as csvfile:
                    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(row)
    except IOError:
        headers = ['repository_name', 'date', op, 'unique_visitors']
        with open(csv_file_name, 'a') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(headers)

        for i in dates_and_op:
            row = [repo_name, i, dates_and_op[i][0], dates_and_op[i][1]]
            with open(csv_file_name, 'a') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(row)

    return ''


def main(username, repo='ALL', op='clones', save_csv='save_csv'):
    """Query the GitHub Traffic API
    :param username: string - GitHub username
    :param repo: string - GitHub user's repo name or by default 'ALL' repos
    :param save_csv: string - Specify if CSV log should be saved
    :return:
    """
    username = username.strip()
    repo = repo.strip()
    op = op.strip()
    pw = getpass.getpass('Password:')
    auth_pair = (username, pw)
    traffic_headers = {'Accept': 'application/vnd.github.spiderman-preview'}

    if repo:
        traffic_response = send_request('traffic', auth_pair, repo, op, traffic_headers)
        traffic_response = traffic_response.json()
        csv_file_name = csv_clones if op == 'clones' else csv_views
        if traffic_response.get('message'):
            print(traffic_response['message'])
            return 'Code done'
        print(json_to_table(repo, traffic_response, op))
        if save_csv == 'save_csv':
            store_csv(repo, traffic_response, csv_file_name, op)

    return ''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='Github username')
    parser.add_argument('repo', help='User\'s repo')
    parser.add_argument('op', help='Traffic operation')
    parser.add_argument('save_csv', help='Set to "no_csv" if no CSV should be saved')
    args = parser.parse_args()
    main(args.username, args.repo, args.op, args.save_csv)