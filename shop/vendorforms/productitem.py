from django import forms
from shop.models import ProductItem, Product, Color, Size
from cloudinary.forms import CloudinaryFileField


class ProductItemForm(forms.ModelForm):
    product_image = CloudinaryFileField(options={"folder": "product-images"})

    class Meta:
        model = ProductItem
        fields = [
            "product",
            "sku",
            "quantity_in_stock",
            "description",
            "product_image",
            "color",
            "size",
            "price",
        ]

        # widgets = {
        #     "product": forms.ModelChoiceField(attrs={"readonly": True}),
        # }

    def __init__(self, *args, **kwargs):
        # product = kwargs.pop('product', None)
        # print('Product in form:', product)
        super(ProductItemForm,self).__init__(*args, **kwargs)
        self.fields['product'] = forms.ModelChoiceField(
            queryset=Product.objects.filter(pk=self.initial['product'].id),
            widget=forms.Select(attrs={"readonly": True}), empty_label=None
        )
        self.fields['product'].widget.attrs['readonly'] = True
        
        self.fields["color"] = forms.ModelChoiceField(
            queryset=Color.objects.all(), empty_label=None
        )
        self.fields["size"] = forms.ModelChoiceField(
            queryset=Size.objects.all(), empty_label=None
        )
        self.fields["sku"] = forms.CharField(initial="SKU will be generated automatically", widget=forms.TextInput(attrs={"readonly": True}))
        
        # self.fields["sku"].widget.attrs.update({"class": "form-control"})
        # self.fields["quantity_in_stock"].widget.attrs.update({"class": "form-control"})
        # self.fields["description"].widget.attrs.update({"class": "form-control"})
        # self.fields["product_image"].widget.attrs.update({"class": "form-control"})
        # self.fields["color"].widget.attrs.update({"class": "form-control"})
        # self.fields["size"].widget.attrs.update({"class": "form-control"})
        # self.fields["price"].widget.attrs.update({"class": "form-control"})
        # for field_name, field in self.fields.items():
        #     if isinstance(field.widget, forms.HiddenInput):
        #         field.required = False

    def clean(self):
        cleaned_data = super().clean()

        # Check if hidden fields are present in the cleaned data
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.HiddenInput):
                if field_name not in cleaned_data:
                    cleaned_data[field_name] = None 

        if self.instance and self.instance.pk:
            cleaned_data["product"] = self.instance.product
        return cleaned_data


class ProductItemFormVariation1(ProductItemForm):
    class Meta(ProductItemForm.Meta):
        # exclude = ["color", "size"]
        widgets = {
            # "product": forms.HiddenInput(),
            # "color": forms.HiddenInput(),
            # "size": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['color'].initial = self.initial['color']
        # self.fields['size'].initial = self.initial['size']
        self.fields['color'] = forms.ModelChoiceField(
            queryset=Color.objects.filter(pk=self.initial['color'].id),
            widget=forms.Select(attrs={"readonly": True}), empty_label=None
        )
        self.fields['size'] = forms.ModelChoiceField(
            queryset=Size.objects.filter(pk=self.initial['size'].id),
            widget=forms.Select(attrs={"readonly": True}), empty_label=None
        )
        # self.fields['color'].initial = Color.objects.get(name='Default')
        # self.fields['size'].initial = Size.objects.get(title='Default')
        # self.fields["product"].widget = forms.HiddenInput()
        # self.fields["color"].widget = forms.HiddenInput()
        # self.fields["size"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        # Check if hidden fields are present in the cleaned data
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.HiddenInput):
                if field_name not in cleaned_data:
                    cleaned_data[field_name] = None

        product = cleaned_data.get("product")
        # Validate against existing product items with the same variation
        if ProductItem.objects.filter(
            product=product,
            color=self.fields["color"].initial,
            size=self.fields["size"].initial,
        ).exists():
            raise forms.ValidationError(
                "A product item with this variation already exists."
            )
        # if ProductItem.objects.filter(
        #     product=product,
        #     color=self.fields["color"].initial,
        #     size=self.fields["size"].initial,
        # # ).exists():
        #     raise forms.ValidationError(
        #         "A product item with this variation already exists."
        #     )

        return cleaned_data


# class ProductItemFormVariation1(forms.ModelForm):
#     class Meta:
#         model = ProductItem
#         fields = [
#             "product",
#             "sku",
#             "quantity_in_stock",
#             "description",
#             "product_image",
#             "color",
#             "size",
#             "price",
#         ]

#     widgets = {
#             "product": forms.HiddenInput(),
#             "color": forms.HiddenInput(),
#             "size": forms.HiddenInput(),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.fields["color"] = forms.ModelChoiceField(
#         #     queryset=Color.objects.all(), empty_label=None
#         # )
#         # self.fields["size"] = forms.ModelChoiceField(
#         #     queryset=Size.objects.all(), empty_label=None
#         # )
#         self.fields["product"].widget = forms.HiddenInput()
#         self.fields["sku"].widget.attrs.update({"class": "form-control"})
#         self.fields["quantity_in_stock"].widget.attrs.update({"class": "form-control"})
#         self.fields["description"].widget.attrs.update({"class": "form-control"})
#         self.fields["product_image"].widget.attrs.update({"class": "form-control"})
#         self.fields["color"].widget = forms.HiddenInput()
#         self.fields["size"].widget = forms.HiddenInput()
#         self.fields["price"].widget.attrs.update({"class": "form-control"})


#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         default_color = Color.objects.get(name="Default")
#         default_size = Size.objects.get(title="Default")
#         instance.color = default_color
#         instance.size = default_size
#         instance.product = self.cleaned_data.get('product')
#         if commit:
#             instance.save()
#         return instance

#     def clean(self):
#         cleaned_data = super().clean()
#         product = cleaned_data.get("product")
#         default_color = Color.objects.get(name="Default")
#         default_size = Size.objects.get(title="Default")
#         if ProductItem.objects.filter(
#             product=product,
#             color=default_color,
#             size=default_size,
#         ).exists():
#             raise forms.ValidationError(
#                 "A product item with this variation already exists."
#             )
#         return cleaned_data


class ProductItemFormVariation2(ProductItemForm):
    class Meta(ProductItemForm.Meta):
        widgets = {
            "color": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_color = Color.objects.get(name="Default")
        self.fields["color"].initial = default_color
        self.fields["color"].label = ""

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        if (
            not ProductItem.objects.filter(product=product)
            .exclude(color=self.fields["color"].initial)
            .exists()
        ):
            raise forms.ValidationError(
                "All product items of this product must have color set to default."
            )
        return cleaned_data


class ProductItemFormVariation3(ProductItemForm):
    class Meta(ProductItemForm.Meta):
        widgets = {
            "size": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_size = Size.objects.get(title="Default")
        self.fields["size"].initial = default_size
        self.fields["size"].label = ""

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        if ProductItem.objects.filter(
            product=product, size=self.fields["size"].initial
        ).exists():
            raise forms.ValidationError(
                "A product item with this size variation already exists."
            )
        return cleaned_data
