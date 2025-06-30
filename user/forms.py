from django.contrib.auth.models import User

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field

class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(max_length=254, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
                Div(
                    Field('username', label="User Name", css_class='form-control-lg'),
                    Field('first_name', label="First Name", css_class='form-control-lg'),
                    Field('last_name', label="Last Name", css_class='form-control-lg'),
                ),
                Field('email', label="Email", css_class='form-control-lg', help_text="We'll never share your email with anyone else."),
                Submit('submit', 'Save Changes', css_class="btn btn-dark btn-block w-100 "),
            )
    
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if self.instance.username != username and User.objects.filter(username=username).exists:
    #         raise forms.ValidationError("This username is already taken.")
    #     return username
    
    
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if self.instance.email != email and User.objects.filter(email=email).exists:
    #         raise forms.ValidationError("This email is already registered.")
    #     return email