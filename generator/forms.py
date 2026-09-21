from django import forms

STYLE_CHOICES = [
    ('Realistic', 'Realistic'),
    ('Cinematic', 'Cinematic'),
    ('Anime', 'Anime'),
    ('Digital Art', 'Digital Art'),
    ('Fantasy', 'Fantasy'),
    ('3D Render', '3D Render'),
]

ASPECT_RATIO_CHOICES = [
    ('1:1', '1:1 (Square)'),
    ('16:9', '16:9 (Landscape)'),
    ('4:3', '4:3 (Standard)'),
    ('3:4', '3:4 (Portrait)'),
    ('9:16', '9:16 (Story / Mobile)'),
]

class ImageGenerationForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'prompt-input',
            'rows': 4,
            'placeholder': 'Describe what you want to create...',
            'class': 'form-control form-textarea',
            'maxlength': '1000',
        }),
        min_length=3,
        max_length=1000,
        required=True,
        error_messages={
            'required': 'Please enter an image description.',
            'min_length': 'Prompt must be at least 3 characters long.',
            'max_length': 'Prompt must be 1000 characters or less.',
        }
    )
    style = forms.ChoiceField(
        choices=STYLE_CHOICES,
        widget=forms.Select(attrs={
            'id': 'style-select',
            'class': 'form-control form-select',
        }),
        required=True,
        initial='Realistic',
        error_messages={
            'required': 'Please select an image style.',
            'invalid_choice': 'Please select a valid image style.',
        }
    )
    aspect_ratio = forms.ChoiceField(
        choices=ASPECT_RATIO_CHOICES,
        widget=forms.Select(attrs={
            'id': 'aspect-ratio-select',
            'class': 'form-control form-select',
        }),
        required=True,
        initial='1:1',
        error_messages={
            'required': 'Please select an aspect ratio.',
            'invalid_choice': 'Please select a valid aspect ratio.',
        }
    )

    def clean_prompt(self):
        prompt = self.cleaned_data.get('prompt', '').strip()
        if not prompt:
            raise forms.ValidationError('Please enter an image description.')
        if len(prompt) > 1000:
            raise forms.ValidationError('Prompt must be 1000 characters or less.')
        return prompt
