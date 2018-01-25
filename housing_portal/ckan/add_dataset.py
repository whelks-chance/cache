import json
import re
import requests
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

    def add_dataset(self, metadata, tags):

        extras = []
        for key, value in tags.items():
            print(key, value)
            extras.append({
                'key': key,
                'value': value
            })

# \x2D - minus
# \x20 space
# \x55 dash
# \x137 underscore
#         TODO add allowed chars back into this regex

        dataset_dict = {
            'name': re.sub(
                r'[^\x61-\x7A]|\x40|\x55|\x137', r'',
                tags['dataset_name'].lower().replace(' ', '-')
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
            "notes": None,
            "extras": extras,
            "title": tags['dataset_name'],
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
        # print(response.content)
        print(response.text)

        # response_dict = response.json()
        # print(response_dict)

        # package_create returns the created package as its result.
        # created_package = response_dict['result']
        # pprint.pprint(created_package)

    def add_resource(self, filepath):
        response = requests.post(
            settings.ckan_url + '/api/action/resource_create',
            data={"package_id": "my_dataset_name"},
            headers={"X-CKAN-API-Key": settings.ckan_api_key},
            files=[('upload', open(filepath, 'rb'))]
        )
        print(response.text)


if __name__ == '__main__':
    ad = AddDataset()

    tags = {
        'timestamp': '12/15/2015 17:22:29',
        'entered_by': 'Sarah',
        'dataset_name': 'Annual Survey of Hours and Earnings Pensions categories (Annual Survey of Hours and Earnings (ASHE))',
        'data_owner': 'ONS',
        'category1': '1 - People',
        'category2': '1.1 - Demographics, social',
        'category_notes': 'Primarily concerns earnings and hours so broader than cost, price and rent',
        'source_of_information': '',
        'source_weblink': 'http://www.ons.gov.uk/ons/rel/ashe/annual-survey-of-hours-and-earnings-pension-tables/index.html',
        'dataset_content': '1% sample of employee jobs taken from HM Revenue & Customs (HMRC) Pay As You Earn (PAYE) records. ASHE does not cover the self-employed nor does it cover employees not paid during the reference period. In 2015 information related to the pay period.  Sample size: 180,000 employee jobs',
        'geographic_coverage': '1 - UK',
        'geographic_units': 'National',
        'geography_notes': '',
        'time_period_from': '1998',
        'time_period_to': 'On-going',
        'time_frequency': 'Annual',
        'time_notes': 'The ASHE replaced the New Earnings Survey (NES) which was administered by the ONS since the 1970s.',
        'data_type': 'Sample survey',
        'data_type_notes': 'Estimates on the levels and distribution of earnings and hours for employees in the UK. Estimates are available for a variety of breakdowns by age groups, gender, industry, and pension type.',
        'data_quality': 'Primary weaknesses identified by ONS include: lack of personal demographic data, timing and periodicity, no coverage of self employed and quality of estimates and low levels of disaggregation can be poor.',
        'data_access': 'Free to download from the ONS',
        'data_owner_attitude_to_research_use': '',
        'other_notes': ''
    }
    ad.add_dataset({}, tags)

    filepath = '/home/ianh/PycharmProjects/cache/housing_portal/ckan/metadata.csv'
    # ad.add_resource(filepath)
