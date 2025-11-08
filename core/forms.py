from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserMetadata

INTEREST_CHOICES = [
    ('hiking', 'Hiking'),
    ('movies', 'Movies'),
    ('food', 'Food'),
    ('reading', 'Reading'),
    ('gaming', 'Gaming'),
]

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)
    interests = forms.ChoiceField(choices=INTEREST_CHOICES, required=True)
    drives = forms.BooleanField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", 
                  "password1", "password2", "interests", "drives", "bio")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")

        metadata_defaults = {
            "interests": self.cleaned_data.get("interests"),
            "drives": self.cleaned_data.get("drives", False),
            "bio": self.cleaned_data.get("bio"),
        }

        if commit:
            user.save()
            UserMetadata.objects.update_or_create(
                user=user,
                defaults=metadata_defaults,
            )

        return user
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserMetadata
        fields = ['bio', 'interests', 'drives']  # add any other fields you want editable
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'interests': forms.TextInput(attrs={'size': 50}),
            'drives': forms.Select(choices=[(True, 'Yes'), (False, 'No')])
        }
        help_texts = {
            'bio': 'Tell us something interesting about yourself.',
            'interests': 'What are your hobbies or interests?',
            'drives': 'Do you drive?'
        }