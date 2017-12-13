import json

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from housing_portal.ckan.ckan_reader import CKANdata


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

    return HttpResponse(json.dumps(datahub_service, indent=4), content_type="application/json")


def ckan_resource(request):
    ckan_resource_uuid = request.GET.get('uuid', 'MISSING CKAN RESOURCE UUID')
    datahub_service = {}
    if ckan_resource_uuid:
        ckan_data = CKANdata()
        ckan_datasets = ckan_data.get_resource_by_uuid(ckan_resource_uuid)
        datahub_service['data'] = ckan_datasets
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
