from django.shortcuts import redirect
from django.views.generic import TemplateView


def home(request):
    # Redirect to the API root
    return redirect('api-root')


class WelcomeView(TemplateView):
    template_name = 'base.html'
