from django import forms

class PolyForm(forms.Form):
    poly_text = forms.CharField(label='Poly Text', max_length=20)
