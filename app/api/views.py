from django.http import JsonResponse
from patients.models import Patient


def get_all(request):
    patients = Patient.objects.all().values()

    return JsonResponse({'patients': list(patients)})