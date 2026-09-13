from django import forms


class BorrowForm(forms.Form):
    library_code = forms.CharField(max_length=50)
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)


class ReturnForm(forms.Form):
    library_code = forms.CharField(max_length=50)