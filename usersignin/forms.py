from django import forms
from django.contrib.auth.models import User

class CustomSignupForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    def signup(self, request, user):
        """
        This method is used to process the signup form data and create a new user.

        Parameters:
            - request: The request object that contains information about the current HTTP request.
            - user: The User object that needs to be updated with the signup form data.

        Returns:
            - None. The method updates the user object directly.

        Note:
            - This method assumes that the form data has already been cleaned and validated.
            - The full_name field is expected to contain both first and last names separated by a space.
        """
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.first_name, user.last_name = self.cleaned_data['full_name'].split()[:2]
        user.set_password(self.cleaned_data['password'])
        user.save()