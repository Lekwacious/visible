from django import forms
from .models import Profile


class ProfileModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar', 'city', 'country', 'gender', 'school', 'work_place', 'date_of_birth')


class SearchForm(forms.Form):
    query = forms.CharField()