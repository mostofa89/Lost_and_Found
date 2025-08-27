from django.shortcuts import render
# Create your views here.


def register(request):
    if request.method == 'POST':
        # Handle form submission
        pass

    return render(request, 'users/register.html')