from django import forms
from .models import WorkspaceInvite


class WorkspaceInviteForm(forms.ModelForm):
    class Meta:
        model = WorkspaceInvite
        fields = ['email', 'role']