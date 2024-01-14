from django import forms
from .models import Product, ProductAttachment
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


input_css_class = 'form-control'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','handle','price']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']=input_css_class

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image','name', 'handle','price']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']=input_css_class

class ProductAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProductAttachment
        fields = ['file','name', 'isFree','active']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            if field in ['isFree','active']:
                continue
            self.fields[field].widget.attrs['class']=input_css_class

ProductAttachmentModelFormSet = modelformset_factory(
    ProductAttachment,
    form = ProductAttachmentForm,
    fields = ['file','name', 'isFree','active'],
    extra=0,
    can_delete=True
)

ProductAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductAttachment,
    form = ProductAttachmentForm,
    formset=ProductAttachmentModelFormSet,
    fields = ['file','name', 'isFree','active'],
    extra=0,
    can_delete=True
)