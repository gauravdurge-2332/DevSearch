from django.forms import ModelForm, widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile, Skills , Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        label = {
            "first_name": "Name",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for names, fields in self.fields.items():
            fields.widget.attrs.update({"class": "input"})


class ProfileForm(ModelForm):
    class Meta:
        model = Userprofile
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for names, fields in self.fields.items():
            fields.widget.attrs.update({"class": "input"})


class SkillForm(ModelForm):
    class Meta:
        model = Skills
        exclude = ["owner"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for names, fields in self.fields.items():
            fields.widget.attrs.update({"class": "input"})

class MessageForm(ModelForm):
    class Meta :
        model = Message 
        fields = ["name" , "email" , "subject" , "body"]
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for names, fields in self.fields.items():
                fields.widget.attrs.update({"class": "input"})