from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostFormArtcl(forms.ModelForm):
    # text = forms.CharField(min_length=20)  # another way

    class Meta:
        model = Post
        fields = ('title', 'author_id', 'category_id', 'text')  # __all__

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        if description is not None and len(description) < 20:
            raise ValidationError({
                "text": "Text must be more than 20 symbols."
            })

        return cleaned_data


class PostFormNews(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author_id', 'category_id', 'text')

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        if description is not None and len(description) < 20:
            raise ValidationError({
                "text": "Text must be more than 20 symbols."
            })

        return cleaned_data
