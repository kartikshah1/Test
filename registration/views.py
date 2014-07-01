"""
    Contains views for the Registration app
"""
import sys
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from elearning_academy import settings
from user_profile.models import CustomUser

from registration.models import ForgotPassword
from user_profile.models import Company
from user_profile.models import Work
from user_profile.models import UserProfile
from registration.models import Registration

from registration.serializers import UserSerializer

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    model = User
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    ##NOTE: This is one big hack, meant to get it running for
    ## the teacher training workshop
    ## A more cleaner way would be to serialize every model
    ## and hence a lot TODO
    def create(self, request):
        data = request.DATA
        username = data.get('username', None)
        password = data.get('password', None)
        email = data.get('email', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        try:
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        is_active=True
                        )
            user.set_password(password)
            user.save()
        except Exception as e:
            message = {'error': str(e), 'error_message': "Error saving model"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        try:
            mobile = data.get('mobile', None)
            city = data.get('city', None)
            user_profile = UserProfile(user=user)
            user_profile.mobile = mobile
            user_profile.city = city
            user_profile.save()
        except Exception as e:
            user.delete()
            message = {'error': str(e), 'error_message': "Error saving model"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        request.user = user
        user_lst = User.objects.filter(username=username, email=email)
        if len(user_lst) == 0:
            error = True
            error_message = "Please enter valid user details"
            errors = {'error': error, 'error_message': error_message}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = user_lst[0]
            fp_object_lst = ForgotPassword.objects.filter(user=user)
            if len(fp_object_lst) == 0:
                fp_object = ForgotPassword(user=user)
                fp_object.generate_key(request)
            else:
                fp_object = fp_object_lst[0]
                fp_object.generate_key(request)
            fp_object.save()
            user_company = data.get('remoteid', None)
            user_company_desc = data.get('remotecentrename', None)
            if user_company is None:
                user.delete()
                error_message = "Remote ID Missing"
                errors = {'error': True, 'error_message': error_message}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            company = Company.objects.filter(company=user_company)
            if (len(company) == 0):
                company = Company()
                company.company = user_company
                company.save()
                user_company = company
            else:
                user_company = company[0]
            user_work = Work(user=user)
            user_work.company = user_company
            user_work.company_description = user_company_desc
            user_work.save()

            return Response({"alldone": "All"}, status=status.HTTP_201_CREATED)


class RegistrationForm(forms.ModelForm):
    """ Registration form """
    # TODO: Find a better way to pass the class value, not from view
    attrs = {'placeholder': 'Select a Username', 'class': 'form-control'}
    username = forms.CharField(widget=forms.TextInput(attrs=attrs))
    attrs['placeholder'] = 'First name'
    first_name = forms.CharField(widget=forms.TextInput(attrs=attrs))
    attrs['placeholder'] = 'Last name'
    last_name = forms.CharField(widget=forms.TextInput(attrs=attrs))
    attrs['placeholder'] = 'Email address'
    email = forms.EmailField(widget=forms.TextInput(attrs=attrs))
    attrs['placeholder'] = 'Choose a Password'
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class LoginForm(forms.Form):
    """ Login form """
    attrs = {'placeholder': 'Username', 'class': 'form-control'}
    username = forms.CharField(widget=forms.TextInput(attrs=attrs))
    attrs['placeholder'] = 'Password'
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))


class ForgotPasswordForm(forms.Form):
    """ Forgot password form """
    attrs = {'placeholder': 'Username', 'class': 'form-control'}
    username = forms.CharField(widget=forms.TextInput(attrs=attrs))
    attrs['placeholder'] = 'Email address'
    email = forms.CharField(widget=forms.TextInput(attrs=attrs))


class ChangePasswordForm(forms.Form):
    """ Change password form """
    attrs = {'placeholder': 'Password', 'class': 'form-control'}
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))
    attrs['placeholder'] = 'Re-enter password'
    re_password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))


def render_login_page(request, register_form=None, login_form=None,
                      parameters={}, next=None):
    """
    Helper function to pass the login and registration forms and render
    the main page
    """
    if register_form is None:
        register_form = RegistrationForm()
    if login_form is None:
        login_form = LoginForm()
    form = {'reg_form': register_form, 'login_form': login_form}
    parameters.update(form)
    parameters['next'] = next
    if 'login' not in parameters and 'signup' not in parameters:
        parameters['login'] = 'active'
    return render(request, 'registration/login.html', parameters)


def login_(request):
    """
    If .../login/ is accessed by GET, show the login and registration form
    If it is accessed by POST, try to login the user and redirect as necessary
    """
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'GET':
        if 'next' in request.GET.keys():
            next = request.GET['next']
        else:
            next = None
        return render_login_page(request, parameters={'login': 'active'},
                                 next=next)
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            error = False
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    customuser = CustomUser.objects.get(user=user)
                    request.session['mode'] = customuser.default_mode
                    print request.session['mode']
                    if 'next' in request.GET.keys():
                        next_url = request.GET["next"]
                    else:
                        next_url = None
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    error = True
                    error_message = "Please activate your account first"
            else:
                error = True
                error_message = "Invalid username / password"
            parameters = {
                'error': error,
                'error_message': error_message,
                'login': 'active'
            }
        else:
            error = True
            error_list = True
            error_message = []
            if request.POST["username"] == "":
                error_message.append("Username is required")
            if request.POST["password"] is None:
                error_message.append("Password is required")
            parameters = {
                'error': error,
                'error_list': error_list,
                'error_message': error_message
            }
        return render_login_page(request, parameters=parameters)
    else:
        raise Http404


def signup(request):
    """
    Register the user and log him in
    """
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'GET':
        return render_login_page(request, parameters={'signup': 'active'})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            user = User(username=username,
                        first_name=form.cleaned_data["first_name"],
                        last_name=form.cleaned_data["last_name"],
                        email=email,
                        is_active=False
                        )
            user.set_password(password)
            user.save()
            registration = Registration(user=user)
            try:
                registration.register(request)
                registration.save()
            except:
                print sys.exc_info()[0]
                user.delete()
                error = True
                error_message = ["Unable to Register user"]
                errors = {
                    'error': error,
                    'error_list': True,
                    'error_message': error_message, 'signup': 'active'
                }
                return render_login_page(request, register_form=form,
                                         parameters=errors)
            info = {
                'info': True,
                'info_message': 'Successfully registered. \
                Check %s and activate your account.' % (email)}
            return render_login_page(request, parameters=info)
        else:
            error = True
            error_message = []
            for key, value in form.errors.iteritems():
                error_message.append((', '.join(value)))
            errors = {
                'error': error,
                'error_list': True,
                'error_message': error_message, 'signup': 'active'}
            return render_login_page(request, register_form=form,
                                     parameters=errors)
    else:
        raise Http404


def logout_(request):
    """
    Logout the current user
    """
    logout(request)
    return redirect(reverse('login'))


def activate(request, key):
    """
    Fetch Registration record corresponding to activation key and activate \
    user accordingly
    """
    try:
        user_record = Registration.objects.get(activation_key=key)
        user_record.activate()
        parameters = {
            'info': True,
            'info_message': "Successfully activated the account. \
            Go ahead and log in now!"}
        return render_login_page(request, parameters=parameters)
    except:
        parameters = {
            'error': True,
            'error_message': "Could not activate. Please re-check!"}
        return render_login_page(request, parameters=parameters)


def render_forgotpassword_page(request, textdisplay=False,
                               formdisplay=False, parameters={}):
    """
    Display the form to enter username and dob for the user to change or \
    set new password
    """
    if textdisplay:
        parameters['textdisplay'] = True
        parameters['formdisplay'] = False
    elif formdisplay:
        forgotpassword_form = ForgotPasswordForm()
        form = {'forgotpassword_form': forgotpassword_form}
        parameters.update(form)
        parameters['formdisplay'] = True
        parameters['textdisplay'] = False

    return render(request, 'registration/forgotpassword.html', parameters)


def forgot_password(request):
    """
    If request of type GET then render/ display the form for entering details \
    to change password \
    Else if the request of type POST then add an entry to forgot password \
    table, send email to user's email id and display a message that email \
    has been sent
    """
    if request.method == 'GET':
        return render_forgotpassword_page(request, formdisplay=True)
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            user_lst = User.objects.filter(username=username, email=email)
            if len(user_lst) == 0:
                error = True
                error_message = "Please enter valid user details"
                errors = {'error': error, 'error_message': error_message}
                return render_forgotpassword_page(
                    request, formdisplay=True, parameters=errors)
            else:
                user = user_lst[0]
                fp_object_lst = ForgotPassword.objects.filter(user=user)
                if len(fp_object_lst) == 0:
                    fp_object = ForgotPassword(user=user)
                    fp_object.generate_key(request)
                else:
                    fp_object = fp_object_lst[0]
                    fp_object.generate_key(request)
                fp_object.save()
                display_msg = "An email has been sent to your email address"
                parameters = {'message': display_msg}
                return render_forgotpassword_page(
                    request, textdisplay=True, parameters=parameters)
        else:
            error = True
            error_message = "Please fill all the details"
            errors = {'error': error, 'error_message': error_message}
            return render_forgotpassword_page(
                request, formdisplay=True, parameters=errors)
    else:
        raise Http404


def render_updatepassword_page(request,
                               textdisplay=False,
                               formdisplay=False, parameters={}):
    """
    Display the form to set a new password
    """
    if textdisplay:
        parameters['textdisplay'] = True
        parameters['formdisplay'] = False
    elif formdisplay:
        changepassword_form = ChangePasswordForm()
        form = {'changepassword_form': changepassword_form}
        parameters.update(form)
        parameters['formdisplay'] = True
        parameters['textdisplay'] = False

    return render(request, 'registration/changepassword.html', parameters)


def update_password(request, key):
    """
    Take the url from mail sent to user and display a form if GET request and \
    update the password if POST request
    """
    if request.method == 'GET':
        get_object_or_404(ForgotPassword, activation_key=key)
        parameters = {'key': key}
        return render_updatepassword_page(request, formdisplay=True,
                                          parameters=parameters)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            npassword = form.cleaned_data["password"]
            cnpassword = form.cleaned_data["re_password"]
            if npassword == cnpassword:
                # change password in the database
                fp_object = get_object_or_404(ForgotPassword,
                                              activation_key=key)
                fp_object.update_password(npassword)
                display_message = """Password successfully updated.
                Please login again."""
                parameters = {
                    'info': True,
                    'info_message': display_message}
                return render_login_page(request, parameters=parameters)
            else:
                error = True
                error_message = "Please enter same the password in both fields"
                errors = {'error': error,
                          'error_message': error_message,
                          'key': key}
                return render_updatepassword_page(request, formdisplay=True,
                                                  parameters=errors)
        else:
            error = True
            error_message = "Please fill all the details"
            errors = {'error': error,
                      'error_message': error_message,
                      'key': key}
            return render_updatepassword_page(request,
                                              formdisplay=True,
                                              parameters=errors)
    else:
        raise Http404


def register(request):
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data,
                        status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors,
                        status=status.HTTP_400_BAD_REQUEST)
