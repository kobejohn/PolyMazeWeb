from django import forms


# this stuff should come from a model / db / something else
TEXT_MAX_LENGTH = 10
COMPLEXITY_CHOICES = ((1, '1 (very simple)'),
                      (2, '2'),
                      (5, '5'),
                      (10, '10'),
                      (20, '20'),
                      (50, '50 (actual maze)'))


class PolyForm(forms.Form):
    text = forms.CharField(label='Maze Text',
                           required=True,
                           max_length=TEXT_MAX_LENGTH,
                           widget=forms.Textarea(attrs={'rows': int(TEXT_MAX_LENGTH/2)+1,
                                                        'cols': TEXT_MAX_LENGTH}),
                           help_text='This text will be converted into a maze.')
    complexity = forms.ChoiceField(label='Complexity',
                                   required=True,
                                   choices=COMPLEXITY_CHOICES)
