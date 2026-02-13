from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user=request.user
    context={
        'user':user
    }
    return render(request,'home.html',context)