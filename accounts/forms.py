from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


GENDER_CHOICES = [
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other"),
    ]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

      
class ProfileForm(forms.ModelForm):

    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    pno = forms.CharField(label="Phone no",
        max_length=10,
            widget = forms.TextInput(attrs={'type': 'tel', 'pattern': '[0-9]{10}', 'oninput': 'this.value=this.value.replace(/[^0-9]/g,"")'}))


    class Meta:
        model = CustomUser
        fields =['image','about', 'birth_date', 'location', 'permanent', 'pno', 'qualification', 'gender',]

        

        widgets = {
              'birth_date' : forms.DateInput(attrs={'type': 'date'})
        }

        labels = {
        'permanent': 'Permanent Address',
        'birth_date': 'Date of Birth',
        }
    # class ProfileUpdateForm(forms.ModelForm):
    #     class Meta:
    #         model = Profile
    #         fields = ['image']