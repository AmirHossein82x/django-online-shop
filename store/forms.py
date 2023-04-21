from django import forms


class AddProductToCartForm(forms.Form):
    CHOICES = [(i, str(i))for i in range(1, 30)]
    quantity = forms.TypedChoiceField(choices=CHOICES, coerce=int)
