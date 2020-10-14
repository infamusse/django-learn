from django import forms


# class ProductForm(forms.Form):
#     title = forms.CharField()

from .models import Product


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'content'
        ]

    def clean_title(self):
        data = self.cleaned_data.get('title')
        if len(data) < 4:
            raise forms.ValidationError('No long enough')
        return data
