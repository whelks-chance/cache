from django.shortcuts import render


# Create your views here.
def search(request):
    return render(request, 'search.html', {'create_tech_form': 0})


def test(request):
    return render(request, 'test.html', {'create_tech_form': 0})


def base(request):
    return render(request, 'base.html', {'create_tech_form': 0})


def example(request):
    return render(request, 'example.html', {'create_tech_form': 0})


def search_results(request):
    return render(request, 'search_results.html', {'create_tech_form': 0})
