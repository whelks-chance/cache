from django.shortcuts import render


# Create your views here.
def test(request):
    return render(request, 'test_vis.html', {'create_tech_form': 0})


def bank_share(request):
    return render(request, 'bank_share.html', {'create_tech_form': 0})
