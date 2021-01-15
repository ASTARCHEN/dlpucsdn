from django.shortcuts import render
from account.models import Department, Profile


# Create your views here.
def assignment_index(request):
    return render(request, 'assignment/index.html', {'user': request.user})


def assignment_issue(request):
    return render(request, 'assignment/issue.html', {'user': request.user})
