import pprint

import ckanapi
import requests

from cache.settings import ckan_api_key, ckan_org_name, ckan_user_name, ckan_url
from housing_portal.datasources.generic_source import RemoteDataDefault
from PIL import Image

class CKANdata(RemoteDataDefault):
    def __init__(self):
        RemoteDataDefault.__init__(self)
        self.ckan_api = None

    def init(self):
        if not self.ckan_api:
            self.ckan_api = ckanapi.RemoteCKAN(
                # 'https://datahub.io',
                ckan_url,
                user_agent='ckanapiexample/1.0 (+http://data.wiserd.ac.uk)',
                apikey=ckan_api_key
            )
        return self.ckan_api

    def get_data_dict(self, dataset_id, options, constants):
        print('options', options, 'constants', constants)

        # value_id = 'WIMD2014'
        # geog_id = 'LSOACode'
        # name_id = 'LSOAName'

        value_id = ''
        geog_id = ''
        name_id = ''

        for op in options:
            if op[0] == 'Name_Code':
                name_id = op[1]
            if op[0] == 'Value_Code':
                value_id = op[1]
            if op[0] == 'Geography_Code':
                geog_id = op[1]

        if name_id == '':
            name_id = value_id

        ckan_api = self.init()

        offset = 0
        return_data = {}

        while offset < 2000:

            data = ckan_api.action.datastore_search(resource_id=dataset_id, offset=offset)
            for d in data['records']:

                return_data[d[name_id]] = [
                    {
                        "name": d[name_id],
                        "value": d[value_id],
                        "geography_code": d[geog_id],
                        "data_status": "A",
                        "geography": d[name_id]
                    }
                ]

            offset += 100
        return return_data

    def get_metadata_for_dataset(self, dataset_id):
        pass

    def get_dataset_overview(self, dataset_id):
        ckan_api = self.init()
        data = ckan_api.action.datastore_search(resource_id=dataset_id)

        dimensions = {}
        value_measures = []
        geog_measures = []
        name_measures = []

        for f in data['fields']:
            if f['id'] != '_id':

                value_measures.append(
                    {
                        'id': f['id'],
                        'name': f['id']
                    }
                )
                geog_measures.append(
                    {
                        'id': f['id'],
                        'name': f['id']
                    }
                )
                name_measures.append(
                    {
                        'id': f['id'],
                        'name': f['id']
                    }
                )

        dimensions['Geography'] = {
            "concept": 'Geography',
            "name": 'Geography',
            'measures': geog_measures
        }
        dimensions['Value'] = {
            "concept": 'Value',
            "name": 'Value',
            'measures': value_measures
        }
        dimensions['Name'] = {
            "concept": 'Name',
            "name": 'Name',
            'measures': name_measures
        }

        return_data = {
            'concepts': [],
            'codelists': dimensions,
            'geographies': [
                {
                    'name': 'LSOA',
                    'id': 'lsoa'
                }
            ]
        }

        return return_data

    def keyword_search(self, keyword_string, args=None):

        all_data = []

        ckan_api = self.init()

        organization_list = ckan_api.action.organization_list(id=ckan_org_name, include_datasets=True)

        print('organization_list\n', organization_list, '\n')

        organization_list_for_user = ckan_api.action.organization_list_for_user(id=ckan_user_name, include_datasets=True)

        print('organization_list_for_user\n', organization_list_for_user, '\n')

        for user_org in organization_list_for_user:
            user_org_name = user_org['name']
            organization_show = ckan_api.action.organization_show(id=user_org_name, include_datasets=True)
            # print('organization_show\n', organization_show, '\n')

            for p in organization_show['packages']:
                # print('p.keys\n', p.keys(), p['id'])
                package_data = ckan_api.action.package_show(id=p['id'])

                for r in package_data['resources']:
                    print('\n\nr\n', r)

                    print('\nresource keys', r.keys(), '\n', r['package_id'], r['id'])
                    if 'datastore_active' in r:
                        print('datastore_active', r['datastore_active'])
                        dat = {
                            'id': r['id'],
                            'name': r['name'],
                            'source': 'CKAN_datahub'
                        }
                    all_data.append(r)

                    print(r['format'], type(r['format']))
                    if r['format'] == 'JPEG':
                        img_data = requests.get(r['url'], stream=True)
                        img_data.raw.decode_content = True  # handle spurious Content-Encoding
                        # img = Image.open(img_data.raw)
                        # img.show()

        return all_data

    def get_resource_by_uuid(self, uuid):
        ckan_api = self.init()

        print(ckan_api.action)

        uuid = ckan_api.action.resource_show(id=uuid)

        # print(uuid)

        return [uuid]

    def get_resource_by_search_term(self, search_term):
        ckan_api = self.init()

        print(ckan_api.action)

        uuid = ckan_api.action.package_search(q=search_term)

        print(uuid)
        return [uuid]


if __name__ == '__main__':
    # import ssl
    #
    # print(ssl.OPENSSL_VERSION)

    datahub_service = {}
    search_term = 'thingy'

    ckan_data = CKANdata()

    # ckan_datasets = ckan_data.keyword_search(search_term.lower())
    # ckan_datasets = ckan_data.get_resource_by_uuid('0211a7b2-76c2-40c2-a6f7-f36307915763')
    ckan_datasets = ckan_data.get_resource_by_search_term('a')

    datahub_service['data'] = ckan_datasets
    datahub_service['message'] = 'Success'
    # datahub_service['time'] = ckan_request.elapsed.total_seconds()
    datahub_service['success'] = True

    print(pprint.pformat(datahub_service))