import urllib

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .forms import PolyForm

from .models_no_db import TextMaze


@require_http_methods(['GET', 'POST'])
def index(request):
    context = {'form': PolyForm(), 'image_url': '', 'note': ''}
    if request.method == 'POST':
        form = PolyForm(request.POST)
        if form.is_valid():
            image_params = {'text': form.cleaned_data['text'].encode('utf-8'),
                            'complexity': form.cleaned_data['complexity']}
            context['image_url'] = reverse('home.views.image') + '?' + urllib.urlencode(image_params, )
            context['note'] = 'A maze image should appear below. Right click or tap and hold to save it.'
            context['form'] = form  # reproduce settings after getting a maze
    return render(request, 'index.html', context)


@require_http_methods(['GET'])
def image(request):
    """Convert provided GET parameters into an image."""
    text = request.GET.get('text')
    complexity = request.GET.get('complexity')
    try:
        maze = TextMaze(text, complexity)
    except (ValueError, TypeError, ValidationError):
        return HttpResponseBadRequest()
    response = HttpResponse(content_type='image/png')
    im = maze.generate_image()
    im.save(response, 'PNG')
    return response
