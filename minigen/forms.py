from django import forms
from minigen.models import MCQPost

class MCQPostForm(forms.ModelForm):
    class Meta:
        model = MCQPost
        fields = ['question', 'reference', 'option1', 'option2', 'option3', 'option4', 'answer']
