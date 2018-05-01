import json

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


# Create your views here.
from housing_portal.ckan_tools.ckan_reader import CKANdata


def search(request):
    return render(request, 'search.html', {'create_tech_form': 0})


def test(request):
    return render(request, 'test.html', {'create_tech_form': 0})


def base(request):
    return render(request, 'base.html', {'create_tech_form': 0})


def example(request):
    return render(request, 'example.html', {'create_tech_form': 0})


def search_results(request):
    search_term = request.GET.get('search_term', 'MISSING SEARCH TERM')
    print(search_term)

    return render(request, 'search_results.html', {
        'create_tech_form': 0,
        'search_term': search_term
    })


def eg1(request):
    return render(request, './examples/index.html', {'create_tech_form': 0})


def ckan_search(request):
    search_term = request.GET.get('search_term')
    datahub_service = {}
    if search_term:
        ckan_data = CKANdata()
        ckan_datasets = ckan_data.keyword_search(search_term.lower())
        datahub_service['data'] = ckan_datasets
        datahub_service['message'] = 'Success'
        datahub_service['success'] = True
    else:
        datahub_service['message'] = 'Failure - requires a search term'
        datahub_service['success'] = False
        datahub_service['error_text'] = 'No search term given'
        datahub_service['data'] = []

    # import time
    # time.sleep(9999)

    # return HttpResponseNotFound('<h1>Page not found</h1>')
    return HttpResponse(json.dumps(datahub_service, indent=4), content_type="application/json")


def ckan_resource(request):
    ckan_resource_uuid = request.GET.get('uuid', 'MISSING CKAN RESOURCE UUID')
    datahub_service = {}
    if ckan_resource_uuid:
        ckan_data = CKANdata()
        ckan_resources = ckan_data.get_resource_by_uuid(ckan_resource_uuid)
        datahub_service['data'] = ckan_resources
        datahub_service['message'] = 'Success'
        datahub_service['success'] = True
    else:
        datahub_service['message'] = 'Failure - requires a search term'
        datahub_service['success'] = False

    return render(request, 'resource.html', {
        'ckan_resource': datahub_service,
        'ckan_resource_uuid': ckan_resource_uuid
    })


def map_test(request):
    return render(request, 'map_test.html', {'create_tech_form': 0})


def clean_str(string):
    return string.replace('_-_', '_')


def cleanup(ckan_datasets):
    for idx, d in enumerate(ckan_datasets):
        cleaned = {}
        print(ckan_datasets[idx]['extras'])
        for e in ckan_datasets[idx]['extras']:
            key = clean_str(e['key'])
            value = clean_str(e['value'])
            cleaned[key] = value
        ckan_datasets[idx]['extras_cleaned'] = cleaned
    return ckan_datasets

def ckan_dataset(request):
    ckan_resource_uuid = request.GET.get('uuid', 'MISSING CKAN RESOURCE UUID')
    datahub_service = {}
    if ckan_resource_uuid:
        ckan_data = CKANdata()
        ckan_datasets = ckan_data.get_dataset_by_uuid(ckan_resource_uuid)
        datahub_service['data'] = cleanup(ckan_datasets)
        datahub_service['message'] = 'Success'
        datahub_service['success'] = True
    else:
        datahub_service['message'] = 'Failure - requires a search term'
        datahub_service['success'] = False

    return render(request, 'ckan_dataset.html', {
        'ckan_dataset': datahub_service,
        'ckan_dataset_uuid': ckan_resource_uuid,
    })