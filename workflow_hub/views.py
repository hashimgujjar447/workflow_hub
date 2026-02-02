from django.shortcuts import render

def home(request):
    user=request.user
    context={
        'user':user
    }
    return render(request,'home.html',context)