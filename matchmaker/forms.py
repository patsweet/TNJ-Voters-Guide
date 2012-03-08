from django import forms
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.formsets import formset_factory
from matchmaker.models import *
import re

class RegisterCandidateForm(forms.Form):
    username = forms.CharField(label=u'Username', max_length=30)
    email = forms.EmailField(label=u'Email')
    password1 = forms.CharField(
        label = u'Password',
        widget = forms.PasswordInput()
    )
    password2 = forms.CharField(
        label = u'Repeat Password',
        widget = forms.PasswordInput()
    )
    secretkey = forms.CharField(
        label = u'Login Key',
        max_length =30
        )

    def check_secretkey(self):
        secret = self.cleaned_data['secretkey']
        if secret == "SchoolBoards2012":
            pass
        else:
            raise forms.ValidationError('Please enter an appropriate Login Key.'
                                        'It should be in the email you received.')
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain '
                                        'alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UpdateFamilyForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        exclude = ('candidate')

class UpdateQandA(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('answer',)
        widgets = {
            'answer': forms.Textarea(),
        }

# FORM TO UPDATE THE CANDIATE'S PAGE. SEPARATE FROM ANSWER FORM.
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
        except User.DoesNotExist:
            pass
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    first_name = forms.CharField(label="First name", max_length=55)
    last_name = forms.CharField(label="Last name", max_length=55)
    email = forms.EmailField(label="Email address")
    mugshot = forms.ImageField(required=False)
    party = forms.ModelChoiceField(label=u'Party', queryset=Party.objects.all())
    occupation = forms.CharField(label = u'Occupation', max_length=150, required=False)
    education = forms.CharField(label = u'Education', max_length=200, required=False)
    birthday = forms.DateField(label=u'Birthday', required=False)
    website = forms.URLField(label=u'Website Link', required=False)
    twitter = forms.CharField(label=u'Twitter Handle', max_length=30, required=False)
    facebook = forms.URLField(label=u'Facebook Link', required=False)
    accolades = forms.CharField(label='Accomplishments (limit 255 chars)', max_length=255, widget=forms.Textarea, required=False)
    genStatement = forms.CharField(label=u'Why elect you?', widget = forms.Textarea)
    
    class Meta:
        model = Candidate
        exclude = ('race', 'user')


    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well. 
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile