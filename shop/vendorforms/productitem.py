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

    def __init__(self, *args, **kwargs):
        super(ProductItemForm, self).__init__(*args, **kwargs)
        self.fields["product"] = forms.ModelChoiceField(
            queryset=Product.objects.filter(pk=self.initial["product"].id),
            widget=forms.Select(attrs={"readonly": True}),
            empty_label=None,
        )
        self.fields["product"].widget.attrs["readonly"] = True

        self.fields["color"] = forms.ModelChoiceField(
            queryset=Color.objects.all(), empty_label=None
        )
        self.fields["size"] = forms.ModelChoiceField(
            queryset=Size.objects.all(), empty_label=None
        )
        self.fields["sku"] = forms.CharField(
            initial="SKU will be generated automatically",
            widget=forms.TextInput(attrs={"readonly": True}),
        )

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["color"] = forms.ModelChoiceField(
            queryset=Color.objects.filter(pk=self.initial["color"].id),
            widget=forms.Select(attrs={"readonly": True}),
            empty_label=None,
        )
        self.fields["size"] = forms.ModelChoiceField(
            queryset=Size.objects.filter(pk=self.initial["size"].id),
            widget=forms.Select(attrs={"readonly": True}),
            empty_label=None,
        )

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
        return cleaned_data


class ProductItemFormVariation2(ProductItemForm):
    class Meta(ProductItemForm.Meta):
        widgets = {
            "color": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["color"] = forms.ModelChoiceField(
            queryset=Color.objects.filter(pk=self.initial["color"].id),
            widget=forms.Select(attrs={"readonly": True}),
            empty_label=None,
        )

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
        self.fields["size"] = forms.ModelChoiceField(
            queryset=Size.objects.filter(pk=self.initial["size"].id),
            widget=forms.Select(attrs={"readonly": True}),
            empty_label=None,
        )

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
