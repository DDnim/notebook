from django.shortcuts import render
 
def hello(request):
    context          = {}
    context['hello'] = 'Hello World!2'
    return render(request, 'hello.html', context)