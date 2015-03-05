from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


def serve_500(request):
    return render_to_response('errors/500.html')


@login_required
def serve_404(request):
    return render_to_response('errors/404.html')