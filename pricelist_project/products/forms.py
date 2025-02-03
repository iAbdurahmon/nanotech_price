from .models import Category, Product
from django.forms import ModelForm, TextInput, NumberInput, Textarea


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of Category'
            })
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of Product'
            }),
            "price": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                "placeholder": 'Description'
            })
        }
