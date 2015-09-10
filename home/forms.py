from django import forms

from .models_no_db import TextMaze


class PolyForm(forms.Form):
    # text field
    _max_length = TextMaze.TEXT_MAX
    _max_cols = _max_length
    _max_rows = max(1, _max_length-2)
    text = forms.CharField(label='Maze Text',
                           required=False,
                           max_length=_max_length,
                           widget=forms.Textarea(attrs={'rows': _max_rows,
                                                        'cols': _max_cols}),
                           help_text='This text will be converted into a maze.')

    # complexity field
    _complexity_min = TextMaze.COMPLEXITY_MIN
    _complexity_choices = [[c, str(c)] for c in range(TextMaze.COMPLEXITY_MIN, 1+TextMaze.COMPLEXITY_MAX)]
    if len(_complexity_choices) > 1:
        _complexity_choices[0][1] += ' (more simple)'
        _complexity_choices[-1][1] += ' (more complex)'
    complexity = forms.ChoiceField(label='Complexity',
                                   required=True,
                                   choices=_complexity_choices)
