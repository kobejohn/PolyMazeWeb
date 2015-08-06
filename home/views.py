import itertools
import os
import random
import StringIO

from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PolyForm

import polymaze as pmz


# instead of simple random shapes, use a randomized cycle so they are not
# repeated until all have been used
_supershapes_cycle = list(pmz.SUPERSHAPES_DICT.items())
random.shuffle(_supershapes_cycle)
_supershapes_cycle = itertools.cycle(_supershapes_cycle)


def index(request):
    context = {'hello': 'hello world', 'form': PolyForm()}

    if request.method == 'POST':
        form = PolyForm(request.POST)
        if form.is_valid():
            poly_text = form.cleaned_data['poly_text']
            context['hello'] = poly_text
            image = ascii_string_maze(poly_text)
            context['form'] = form
            response = HttpResponse(content_type='image/png')
            image.save(response, 'PNG')
            # response['Content-Disposition'] = 'attachment; filename=maze.png'
            return response

    return render(request, 'index.html', context)


def ascii_string_maze(s):
    s = s.replace('\n', r'\n')

    supershape_name, supershape = next(_supershapes_cycle)
    grid = pmz.PolyGrid(supershape=supershape)
    grid.create_string(s, complexity=10)
    maze = pmz.Maze(grid)
    image = maze.image()
    # output = StringIO.StringIO()
    # image.save(output, 'PNG')
    # contents = output.getvalue()
    # output.close()
    return image


    #
    # filename = os.path.join('.',
    #                         'ASCII String ({}).png'.format(supershape_name))
    # maze.image().save(filename, format='PNG')
    #

