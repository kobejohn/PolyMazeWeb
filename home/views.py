import itertools
import random

from django.shortcuts import render
from django.http import HttpResponse
from .forms import PolyForm

import polymaze as pmz


# shuffled cycle of shapes to use
_supershapes_cycle = list(pmz.SUPERSHAPES_DICT.items())
random.shuffle(_supershapes_cycle)
_supershapes_cycle = itertools.cycle(_supershapes_cycle)


def index(request):
    context = {'headline': 'Welcome to PolyMaze.', 'form': PolyForm()}
    if request.method == 'POST':
        form = PolyForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            complexity = int(form.cleaned_data['complexity'])  # convert to int just in case string
            image = ascii_string_maze(text, complexity)
            context['form'] = form
            response = HttpResponse(content_type='image/png')
            image.save(response, 'PNG')
            return response
    return render(request, 'index.html', context)


def ascii_string_maze(text, complexity):
    text = text.replace('\n', r'\n')  # polymaze expects literal \n to indicate newlines
    supershape_name, supershape = next(_supershapes_cycle)
    grid = pmz.PolyGrid(supershape=supershape)
    grid.create_string(text, complexity=complexity)
    maze = pmz.Maze(grid)
    image = maze.image()
    return image
