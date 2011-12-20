from django import forms
from django.core.validators import email_re

from django.contrib.auth.models import User

from geonode.maps.models import Map, Layer


class GroupInviteForm(forms.Form):
    
    role = forms.ChoiceField(choices=[
        ("manager", "Manager"),
        ("member", "Member"),
    ])
    user_identifiers = forms.CharField(widget=forms.Textarea)
    
    def clean_user_identifiers(self):
        value = self.cleaned_data["user_identifiers"]
        invitees, errors = [], []
        
        for ui in value.split(","):
            ui = ui.strip()
            
            if email_re.match(ui):
                try:
                    invitees.append(User.objects.get(email=ui))
                except User.DoesNotExist:
                    invitees.append(ui)
            else:
                try:
                    invitees.append(User.objects.get(username=ui))
                except User.DoesNotExist:
                    errors.append(ui)
        
        if errors:
            message = ("The following are not valid email addresses or "
                "usernames: %s; no invitations sent" % ", ".join(errors))
            raise forms.ValidationError(message)
        
        return invitees


class GroupMapForm(forms.Form):
    maps = forms.ModelMultipleChoiceField(queryset=Map.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)


class GroupLayerForm(forms.Form):
    layers = forms.ModelMultipleChoiceField(queryset=Layer.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
