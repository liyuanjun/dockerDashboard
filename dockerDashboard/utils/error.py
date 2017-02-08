from django.shortcuts import render_to_response


def system_404(request):
    return render_to_response('404.html')


def system_500(request):
    return render_to_response('500.html')


