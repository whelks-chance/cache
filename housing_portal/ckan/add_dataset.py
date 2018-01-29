import csv
import getopt
import json
import pprint
import re

import os

import math
import requests
import sys

from cache import settings


class AddDataset:
    def __init__(self):
        self.tags = {
            'timestamp': '',
            'entered_by': '',
            'dataset_name': '',
            'data_owner': '',
            'category1': '',
            'category2': '',
            'category_notes': '',
            'source_of_information': '',
            'source_weblink': '',
            'dataset_content': '',
            'geographic_coverage': '',
            'geographic_units': '',
            'geography_notes': '',
            'time_period_from': '',
            'time_period_to': '',
            'time_frequency': '',
            'time_notes': '',
            'data_type': '',
            'data_type_notes': '',
            'data_quality': '',
            'data_access': '',
            'data_owner_attitude_to_research_use': '',
            'other_notes': ''
        }

    def convert(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower().replace(' ', '_')

    def add_dataset(self, metadata, tags):
        description_keys = [
            'category_notes',
            'dataset_content',
            'source_-_weblink',
            'time_notes',
            'data_type_notes',
            'data_quality',
            'data_access'
        ]

        description = ''
        extras = []
        tags_cleaned = {}

        for key, value in tags.items():
            print('converting', key, self.convert(key), value)
            if value:
                extras.append({
                    'key': self.convert(key),
                    'value': value
                })
                tags_cleaned[self.convert(key)] = value

        for description_key in description_keys:
            if description_key in tags_cleaned:
                description += '\n\n' + tags_cleaned[description_key]
        description = description.strip()

        # \x2D - minus
        # \x20 space
        # \x55 dash
        # \x137 underscore
        #         TODO add allowed chars back into this regex

        dataset_dict = {
            'name': re.sub(
                r'[^\x61-\x7A]|\x40|\x55|\x137', r'',
                tags_cleaned['dataset_name'].lower()
            ),
            'owner_org': settings.ckan_org_name,

            "license_title": None,
            "maintainer": None,
            "private": False,
            "maintainer_email": None,
            "num_tags": 0,
            "author": None,
            "author_email": None,
            "state": "active",
            "version": None,
            "type": "dataset",
            "resources": [
            ],
            "num_resources": 0,
            # "tags": [tags],
            "groups": [
            ],
            "license_id": None,
            "isopen": None,
            "url": None,
            "notes": description,
            "extras": extras,
            "title": tags_cleaned['dataset_name'],
        }

        # Make the HTTP request.
        response = requests.post(
            settings.ckan_url + '/api/action/package_create',
            headers={
                'Authorization': settings.ckan_api_key,
                'content-type': 'application/json'
            },
            data=json.dumps(dataset_dict))
        print(response.status_code)
        print(response.reason)
        print(response.content)
        print(response.text)

        response_dict = response.json()
        # print(response_dict)

        # package_create returns the created package as its result.
        # created_package = response_dict['result']
        # pprint.pprint(created_package)

        dataset_name = ''
        try:
            print('Added', response_dict['result']['name'])
            pprint.pformat(response_dict)
            dataset_name = response_dict['result']['name']

        except:
            dataset_name = re.sub(
                r'[^\x61-\x7A]|\x40|\x55|\x137', r'',
                tags_cleaned['dataset_name'].lower().replace(' ', '-')
            )

        if tags_cleaned['source_-_weblink']:
            for url in tags_cleaned['source_-_weblink'].split('\n'):
                url = url.strip()
                if ' ' not in url:
                    self.add_resource(
                        "Source - weblink",
                        dataset_name,
                        None,
                        url
                    )

        return response.json()

    def add_resource(self, resource_name, dataset_name, filepath, url):
        data = json.dumps(
            {
                "package_id": dataset_name,
                "url": url,
                "name": resource_name,
                "format": "text/html"
            })
        print('\n\n', data, '\n\n')

        response = requests.post(
            settings.ckan_url + '/api/action/resource_create',
            data=data,
            headers={
                "X-CKAN-API-Key": settings.ckan_api_key,
                'content-type': 'application/json'
            }
            # files=[('upload', open(filepath, 'rb'))]
        )
        print(response.text)

    def add_csv_dataset(self, csv_filepath, limit=None):
        with open(csv_filepath,  'r', encoding="latin-1") as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            csv_file.seek(0)
            print('dialect', dialect)
            dr = csv.DictReader(csv_file)
            print(dr.fieldnames)

            count = 0
            for row in dr:
                count += 1
                if limit and count > limit:
                    break
                ad.add_dataset({}, row)


if __name__ == '__main__':

    ad = AddDataset()
    for arg in sys.argv:
        print(arg)

    inputfile = './metadata.csv'
    outputfile = ''
    try:
        opts, args = getopt.getopt(sys.argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if os.path.isfile(inputfile):
        print('Input file is ', inputfile)
    else:
        print('Input file missing or unavailable')

    ad.add_csv_dataset(inputfile, limit=None)
    exit()

    # tags = {
    #     'timestamp': '12/15/2015 17:22:29',
    #     'entered_by': 'Sarah',
    #     'dataset_name': 'Annual Survey of Hours and Earnings Pensions categories (Annual Survey of Hours and Earnings (ASHE))',
    #     'data_owner': 'ONS',
    #     'category1': '1 - People',
    #     'category2': '1.1 - Demographics, social',
    #     'category_notes': 'Primarily concerns earnings and hours so broader than cost, price and rent',
    #     'source_of_information': '',
    #     'source_weblink': 'http://www.ons.gov.uk/ons/rel/ashe/annual-survey-of-hours-and-earnings-pension-tables/index.html',
    #     'dataset_content': '1% sample of employee jobs taken from HM Revenue & Customs (HMRC) Pay As You Earn (PAYE) records. ASHE does not cover the self-employed nor does it cover employees not paid during the reference period. In 2015 information related to the pay period.  Sample size: 180,000 employee jobs',
    #     'geographic_coverage': '1 - UK',
    #     'geographic_units': 'National',
    #     'geography_notes': '',
    #     'time_period_from': '1998',
    #     'time_period_to': 'On-going',
    #     'time_frequency': 'Annual',
    #     'time_notes': 'The ASHE replaced the New Earnings Survey (NES) which was administered by the ONS since the 1970s.',
    #     'data_type': 'Sample survey',
    #     'data_type_notes': 'Estimates on the levels and distribution of earnings and hours for employees in the UK. Estimates are available for a variety of breakdowns by age groups, gender, industry, and pension type.',
    #     'data_quality': 'Primary weaknesses identified by ONS include: lack of personal demographic data, timing and periodicity, no coverage of self employed and quality of estimates and low levels of disaggregation can be poor.',
    #     'data_access': 'Free to download from the ONS',
    #     'data_owner_attitude_to_research_use': '',
    #     'other_notes': ''
    # }
    # response = ad.add_dataset({}, tags)
    # dataset_name = ''
    # try:
    #     print('Added', response['result']['name'])
    #     pprint.pformat(response)
    #     dataset_name = response['result']['name']
    #
    # except:
    #     dataset_name = re.sub(
    #         r'[^\x61-\x7A]|\x40|\x55|\x137', r'',
    #         tags['dataset_name'].lower().replace(' ', '-')
    #     )

    filepath = '/home/ianh/PycharmProjects/cache/housing_portal/ckan/metadata.csv'
    ad.add_resource(
        "Source - weblink",
        dataset_name,
        filepath,
        tags['source_weblink']
    )

