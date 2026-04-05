from symtable import Class

from django.forms import ModelForm, widgets
from .models import Project , Review
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "demo_link",
            "source_link",
            "featured_image",
            
        ]

        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for names, fields in self.fields.items():
            fields.widget.attrs.update({"class": "input"})


class ReviewForm(ModelForm):
    class Meta:
        model=Review
        fields=["value","body"]

        labels={
            'value' : 'Place your vote' ,
            'body' : 'Add the Comment With Your vote'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for names, fields in self.fields.items():
            fields.widget.attrs.update({"class": "input"})