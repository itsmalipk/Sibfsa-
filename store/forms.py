from django import forms

class CheckoutForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=160)
    phone = forms.CharField(max_length=40)
    line1 = forms.CharField(max_length=200, label="Address line 1")
    line2 = forms.CharField(max_length=200, required=False, label="Address line 2")
    city = forms.CharField(max_length=120)
    region = forms.CharField(max_length=120, label="Region/Province")
    postal_code = forms.CharField(max_length=20)
    country = forms.CharField(max_length=2, initial='PK')

class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    title = forms.CharField(max_length=120)
    body = forms.CharField(widget=forms.Textarea)