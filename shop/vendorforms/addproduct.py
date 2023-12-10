# Designing the Add product Form for vendors that want to add new products to their store
from django import forms
from shop.models import Category, Label, Product, Variation

class AddProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label=None)
    label = forms.ModelChoiceField(queryset=Label.objects.all(), empty_label=None)
    variation = forms.ModelChoiceField(queryset=Variation.objects.all(), empty_label=None)

    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'image', 'variation', 'label', 'price', 'discount_price']

        widgets = {
           'title': forms.TextInput(attrs={
                'placeholder': 'Enter product name',
            }),

            'description': forms.Textarea(attrs={
                'placeholder': 'Enter product description',
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            }),
          
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter price',
            }),
            'discount_price': forms.NumberInput(attrs={
                'placeholder': 'Enter discount price',
            }),
        }

    # def is_textarea(self, field_name):
    #     return isinstance(self.fields[field_name].widget, forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['variation'].required = True
        self.fields['price'].required = True
        self.fields['label'].required = False
 