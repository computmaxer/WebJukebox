from django import forms
from django.contrib.auth.models import User
import actions
from django.utils.safestring import mark_safe

class DateInput(forms.widgets.DateInput):
    """
    Widget for showing a hint title in the field.
    """
    def __init__(self, attrs=None, title=None, format=None):
        if not format:
            format = "%m/%d/%Y"
        forms.widgets.DateInput.__init__(self, attrs, format)

    def render(self, name, value, attrs=None):
        date_attrs = self.build_attrs(attrs)
        input = forms.widgets.DateInput.render(self, name, value, date_attrs)       
        id = date_attrs['id']
        js = '<script type="text/javascript">$(function() { $("#%s").datepicker({ }); });</script>' % id
        return mark_safe(input + js)
    
class DateTimeInput(forms.widgets.SplitDateTimeWidget):
    
    def __init__(self, attrs=None, date_format=None, time_format=None):
        if attrs is None:
            attrs = {}
        attrs['style'] = 'width:96px;'
        date_attrs = attrs.copy()
        date_attrs['placeholder'] = 'MM/DD/YYYY'
        time_attrs = attrs.copy()
        time_attrs['placeholder'] = 'HH:MM (24hr)'
        widgets = (DateInput(attrs=date_attrs, format=date_format),
                   forms.widgets.TimeInput(attrs=time_attrs, format=time_format))
        super(forms.widgets.SplitDateTimeWidget, self).__init__(widgets, attrs)    

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.setup(*args, **kwargs)

    def setup(self, *args, **kwargs):
        """
        To be subclassed.
        Useful for populating a ChoiceField with choices from the database.
        """
        pass


class EventFinderForm(BaseForm):
    zipcode = forms.IntegerField(label='', widget=forms.TextInput(attrs={'placeholder':'Enter your zipcode'}))


class BaseEventForm(BaseForm):
    name = forms.CharField(max_length=50, required=True)
    date_time = forms.DateTimeField(widget=DateTimeInput(),label="Date and Time")
    location = forms.CharField(max_length=100, required=False)
    zipcode = forms.IntegerField(label="Zip Code")


class CreateEventForm(BaseEventForm):
    library_keys = forms.MultipleChoiceField(required=False, choices=[('None', 'None (Setup later)')], initial='None')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateEventForm, self).__init__(*args, **kwargs)

        libraries = actions.get_libraries_for_user(self.user)
        choices = [(str(library.id), library.name) for library in libraries]
        self.fields['library_keys'].choices = choices


class AddLibraryForm(BaseForm):
    name = forms.CharField(max_length=60, required=True)
    file = forms.FileField()
    if not file:
        raise forms.ValidationError("Please choose a file to upload.")


class EditLibraryForm(BaseForm):
    name = forms.CharField(max_length=60, required=True)
    library = forms.CharField(widget=forms.HiddenInput(), label="")


class EditAccountForm(BaseForm):
    def __init__(self, current_user, *args, **kwargs):
        self.user = current_user
        super(EditAccountForm, self).__init__(*args, **kwargs)
    
    email = forms.CharField(label="Email", max_length=100, widget=forms.TextInput(attrs={'class':'disabled', 'readonly':'readonly'}), required=False)
    username = forms.CharField(label="Username", max_length=50, required=False)
    firstname = forms.CharField(label="First Name", max_length=30, required=False)
    lastname = forms.CharField(label="Last Name", max_length=30, required=False)
    streetaddress = forms.CharField(label="Street Address", max_length=100, required=False)
    city = forms.CharField(label="City", max_length=100, required=False)
    zipcode = forms.IntegerField(label="Zipcode", min_value=0, max_value=1000000, required=False)
    is_dj = forms.BooleanField(required=False, initial=False, label='DJ account?')
    
    def clean_username(self):
        cusername = self.cleaned_data['username']
        # check if username is unique
        if (self.user.username != cusername):
            try:
                User.objects.get(username=cusername)
            except User.DoesNotExist:
                return cusername
            raise forms.ValidationError("Username already exists")
        
        return cusername
    

class RegistrationForm(BaseForm):
    email = forms.CharField(label="Email", max_length=100, required=True)
    username = forms.CharField(label="Username", max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    verified_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    is_dj = forms.BooleanField(required=False, initial=False, label='DJ account?')
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        
        password = cleaned_data['password']
        verify = cleaned_data['verified_password']
        cusername = cleaned_data['username']
        
        if(len(password) < 8):
            raise forms.ValidationError("Password must be at least 8 characters")
        if password != verify:
            raise forms.ValidationError("Passwords do not match")
        
        try:
            User.objects.get(username=cusername)
        except User.DoesNotExist:
            return cleaned_data
        raise forms.ValidationError("This username already exists")
        
        return cleaned_data


