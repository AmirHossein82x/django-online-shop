from django import forms
from django.db import transaction
from django.shortcuts import redirect
from phonenumber_field.formfields import PhoneNumberField

from .models import Order, OrderItem, Profile
from .cart import Cart
from core.models import CustomUser


class AddProductToCartForm(forms.Form):
    CHOICES = [(i, str(i)) for i in range(1, 30)]
    quantity = forms.TypedChoiceField(choices=CHOICES, coerce=int)


class OrderCreateForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone_number = PhoneNumberField(region='IR')
    address = forms.CharField(widget=forms.Textarea, max_length=1000)
    note = forms.CharField(max_length=500)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['email'].required = False
        if Order.objects.filter(profile__user=self.request.user).exists():
            self.fields['first_name'].disabled = True
            self.fields['first_name'].required = False
            self.fields['last_name'].disabled = True
            self.fields['last_name'].required = False
            self.fields['phone_number'].disabled = True
            self.fields['phone_number'].required = False
            self.fields['address'].disabled = True
            self.fields['address'].required = False

    def save(self):
        with transaction.atomic():
            cart = Cart(self.request)
            cleaned_data = self.cleaned_data
            if not Order.objects.filter(profile__user=self.request.user).exists():
                CustomUser.objects.filter(id=self.request.user.id).update(first_name=cleaned_data['first_name'],
                                                                          last_name=cleaned_data['last_name'])
                Profile.objects.filter(user=self.request.user).update(address=cleaned_data['address'],
                                                                      phone_number=cleaned_data['phone_number'])
            profile = Profile.objects.get(user=self.request.user)
            order = Order.objects.create(profile=profile, note=cleaned_data['note'], total_price=cart.total_price())
            order_items = [
                OrderItem(
                    order=order,
                    product=item.get('obj'),
                    quantity=item.get('quantity'),
                    price=item.get('price')
                )
                for item in cart
            ]
            OrderItem.objects.bulk_create(order_items)
            cart.clear()


class ProfileForm(forms.Form):
    email = forms.EmailField(disabled=True)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone_number = PhoneNumberField(region='IR')
    address = forms.CharField(widget=forms.Textarea, max_length=1000)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['email'].required = False

    def save(self):
        cleaned_data = self.cleaned_data
        CustomUser.objects.filter(pk=self.request.user.id).update(
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'])

        Profile.objects.filter(user=self.request.user).update(
            phone_number=cleaned_data['phone_number'],
            address=cleaned_data['address'])


