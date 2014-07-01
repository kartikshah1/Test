"""
    Contains views for the user profile app
"""

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import Http404
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.shortcuts import render
from model_utils import Choices

from rest_framework import status


from user_profile.countries import COUNTRIES
from user_profile.models import UserProfile, DEGREE, Education, College, Major, Company, Work
from elearning_academy.settings import MEDIA_ROOT
from elearning_academy.permissions import is_valid_mode

from datetime import date
import json
import os

# Constants
GENDER_CHOICES = Choices(('M', 'Male'), ('F', 'Female'))
BIRTH_YEAR_CHOICES = ('1985', '1986', '1987', '1988', '1989', '1990',
                      '1991', '1992', '1993', '1994', '1995', '1996',
                      '1997', '1998', '1999', '2000', '2001', '2002')
COLLEGE_YEAR_CHOICES = ('1985', '1986', '1987', '1988', '1989', '1990',
                        '1991', '1992', '1993', '1994', '1995', '1996',
                        '1997', '1998', '1999', '2000', '2001', '2002',
                        '2003', '2004', '2005', '2006', '2007', '2008',
                        '2009', '2010', '2011', '2012', '2013')
COLLEGE_YEAR_CHOICES = tuple(reversed(COLLEGE_YEAR_CHOICES))


class ImageForm(forms.Form):
    """
    Profile Image form
    """
    form_method = forms.CharField(widget=forms.HiddenInput(), initial='image')
    image = forms.ImageField(label="Image")


class AboutForm(forms.Form):
    """
        User About form
    """
    form_method = forms.CharField(widget=forms.HiddenInput(), initial='about')
    attrs = {'placeholder': 'First Name', 'class': 'form-control'}
    first_name = forms.CharField(widget=forms.TextInput(attrs=attrs))
    attrs = {'placeholder': 'Last Name', 'class': 'form-control'}
    last_name = forms.CharField(widget=forms.TextInput(attrs=attrs))
    attrs = {'placeholder': 'About you . . .', 'class': 'form-control', 'rows': 2}
    about = forms.CharField(widget=forms.Textarea(attrs=attrs), required=False)
    attrs = {'placeholder': 'What interests you ?', 'class': 'form-control', 'rows': 2}
    interests = forms.CharField(widget=forms.Textarea(attrs=attrs), required=False)


class PersonalInfoForm(forms.Form):
    """
    Personal Information form
    """
    attrs = {'class': 'btn btn-default dropdown-toggle'}
    dob = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES, attrs=attrs),
                          label="Date of Birth", required=False, initial=date(1991, 1, 1))
    attrs = {'class': 'btn btn-default dropdown-toggle'}
    gender = forms.ChoiceField(widget=forms.Select(attrs=attrs), required=False,
                               choices=GENDER_CHOICES, initial=GENDER_CHOICES.M)
    attrs = {'class': 'btn btn-default dropdown-toggle'}
    country = forms.ChoiceField(widget=forms.Select(attrs=attrs), required=False,
                                choices=COUNTRIES, initial=COUNTRIES.IN)
    attrs = {'placeholder': 'State', 'class': 'form-control'}
    state = forms.CharField(widget=forms.TextInput(attrs=attrs), initial='Maharashtra',
                            required=False)
    attrs = {'placeholder': 'City', 'class': 'form-control'}
    city = forms.CharField(widget=forms.TextInput(attrs=attrs), initial='Mumbai',
                           required=False)
    form_method = forms.CharField(widget=forms.HiddenInput(), initial='personal_info')


class AddEducationForm(forms.Form):
    """
        User Education Details - Add
    """
    form_method = forms.CharField(widget=forms.HiddenInput(), initial='add_education')
    attrs = {'placeholder': 'Where did you go to study?',
             'class': 'typeahead tt-query form-control'}
    college = forms.CharField(widget=forms.TextInput(attrs=attrs), required=True)
    attrs = {'placeholder': 'Whats yours major?', 'class': 'typeahead tt-query form-control'}
    major = forms.CharField(widget=forms.TextInput(attrs=attrs), required=True)
    attrs = {'class': 'btn btn-default dropdown-toggle',
             'style': 'font-size: small; width: 100%'}
    degree = forms.ChoiceField(widget=forms.Select(attrs=attrs), required=True,
                               choices=DEGREE, initial=DEGREE.BTECH)
    attrs = {'class': 'btn btn-default dropdown-toggle dropdown-date'}
    start_date = forms.DateField(widget=SelectDateWidget(years=COLLEGE_YEAR_CHOICES, attrs=attrs),
                                 label="From", required=True, initial=date.today())
    attrs = {'class': 'btn btn-default dropdown-toggle dropdown-date'}
    end_date = forms.DateField(widget=SelectDateWidget(years=COLLEGE_YEAR_CHOICES, attrs=attrs),
                               label="To", required=False, initial=date.today())


class AddWorkForm(forms.Form):
    """
        User Work Details - Add
    """
    form_method = forms.CharField(widget=forms.HiddenInput(), initial='add_work')
    attrs = {'placeholder': 'Where did you work ?', 'class': 'typeahead tt-query form-control'}
    company = forms.CharField(widget=forms.TextInput(attrs=attrs), required=True)
    attrs = {'placeholder': 'What was your position ?', 'class': 'form-control'}
    position = forms.CharField(widget=forms.TextInput(attrs=attrs), required=True)
    attrs = {'placeholder': 'Describe your role', 'class': 'form-control', 'rows': 3}
    description = forms.CharField(widget=forms.Textarea(attrs=attrs), required=False)
    attrs = {'class': 'btn btn-default dropdown-toggle dropdown-date'}
    start_date = forms.DateField(widget=SelectDateWidget(years=COLLEGE_YEAR_CHOICES, attrs=attrs),
                                 label="From", required=True, initial=date.today())
    attrs = {'class': 'btn btn-default dropdown-toggle dropdown-date'}
    end_date = forms.DateField(widget=SelectDateWidget(years=COLLEGE_YEAR_CHOICES, attrs=attrs),
                               label="To", required=False, initial=date.today())


class RemoveWorkform(forms.Form):
    """
        User Work Details - Remove
    """
    form_method = forms.CharField(widget=forms.HiddenInput())
    work_id = forms.CharField(widget=forms.HiddenInput())


class RemoveEducationForm(forms.Form):
    """
        User Education Details - Remove
    """
    form_method = forms.CharField(widget=forms.HiddenInput())
    education_id = forms.CharField(widget=forms.HiddenInput())


class SocialForm(forms.Form):
    """
        User social data
    """
    form_method = forms.CharField(widget=forms.HiddenInput(), initial='social')
    attrs = {'placeholder': 'twitter-handle', 'class': 'form-control'}
    twitter = forms.CharField(widget=forms.TextInput(attrs=attrs), required=False,
                              label='Twitter Handle')
    attrs = {'placeholder': 'facebook-username', 'class': 'form-control'}
    facebook = forms.CharField(widget=forms.TextInput(attrs=attrs),
                               required=False, label='Facebook Timeline')


@login_required
def home(request):
    """
        Home page for the user
    """
    return render(request, 'elearning_academy/logged_in.html')


def create_profile(request):
    """
        Display the view-profile for the user whose profile is not yet created
    """
    user = request.user
    error = True
    error_message = "Your profile is empty. Create Now !"
    default_image = "/static/elearning_academy/img/default/user.jpg"
    parameters = {
        'error': error,
        'error_message': error_message
    }
    parameters.update({
        'default_image': default_image,
        'photo': '/media/',
        'user_name': user.get_full_name(),
        'profile_exists': False,
        'about': 'About : Describe yourself !',
        'interests': 'Interests : What excites you ?'
    })
    form = get_update_form(user)
    parameters.update(form)
    print parameters
    return render(request, 'user_profile/profile.html', parameters)


def get_update_form(user):
    """
        Returns dictionary of all forms used in profile page
    """
    user_profile = UserProfile.objects.filter(user=user)
    image_form = ImageForm()

    if len(user_profile) == 0:
        about_form = AboutForm({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'form_method': 'about'
        })
        personal_info_form = PersonalInfoForm()
        add_education_form = AddEducationForm()
        add_work_form = AddWorkForm()
        social_form = SocialForm()
    else:
        user_profile = user_profile[0]
        about_form = AboutForm({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'about': user_profile.about,
            'interests': user_profile.interests,
            'form_method': 'about'
        })

        if user_profile.gender:
            gender = user_profile.gender
        else:
            gender = 'M'
        if user_profile.dob:
            dob = user_profile.dob
        else:
            ##  date(1991, 1, 1)
            dob = None
        if user_profile.place_country:
            country = user_profile.place_country
        else:
            country = 'IN'
        personal_info_form = PersonalInfoForm({
            'gender': gender,
            'dob': dob,
            'city': user_profile.place_city,
            'state': user_profile.place_state,
            'country': country,
            'form_method': 'personal_info'
        })
        add_education_form = AddEducationForm({
            'form_method': 'add_education'
        })
        add_work_form = AddWorkForm({
            'form_method': 'add_work'
        })
        social_form = SocialForm({
            'form_method': 'social',
            'twitter': user_profile.website_twitter,
            'facebook': user_profile.website_facebook
        })

    form = {
        'image_form': image_form,
        'about_form': about_form,
        'personal_info_form': personal_info_form,
        'add_education_form': add_education_form,
        'add_work_form': add_work_form,
        'social_form': social_form
    }
    return form


@login_required
def view_profile(request):
    """
        View the profile for a user
    """
    username = request.user.username
    user = User.objects.get(username=username)
    fullname = user.get_full_name()
    if request.method == 'GET':
        user_profile = UserProfile.objects.filter(user=user)
        if len(user_profile) == 0:
            return create_profile(request)
        else:
            default_image = "/static/elearning_academy/img/default/user.jpg"
            user_profile_dictionary = json.loads(user_profile[0].toJson())
            parameters = {'user_name': fullname,
                          'default_image': default_image,
                          'profile_exists': True}
            parameters.update(user_profile_dictionary)
            form = get_update_form(user)
            parameters.update(form)
            return render(request, 'user_profile/profile.html', parameters)
    elif request.method == 'POST':
        if request.POST['form_method'] == 'image':
            return edit_image(request)
        elif request.POST['form_method'] == 'about':
            return edit_user_intro(request)
        elif request.POST['form_method'] == 'personal_info':
            return edit_user_personal_info(request)
        elif request.POST['form_method'] == 'social':
            return edit_user_social(request)
        elif request.POST['form_method'] == 'add_education':
            return add_user_education(request)
        elif request.POST['form_method'] == 'remove_education':
            return remove_user_education(request)
        elif request.POST['form_method'] == 'add_work':
            return add_user_work(request)
        elif request.POST['form_method'] == 'remove_work':
            return remove_user_work(request)
        else:
            return HttpResponse("No form_method defined. This is error in user_profile/views.py")
    else:
        raise Http404


@login_required
def edit_user_social(request):
    """
        Edit User social details
    """
    user = request.user
    fullname = user.get_full_name()
    form = SocialForm(request.POST)

    user_profile = UserProfile.objects.filter(user=user)
    if len(user_profile) != 0:
        current_user_profile = user_profile[0]
    elif form.is_valid():
        current_user_profile = UserProfile(user=user)
        current_user_profile.generate_user_id()
        current_user_profile.save()

    if form.is_valid():
        current_user_profile.website_twitter = form.cleaned_data["twitter"]
        current_user_profile.website_facebook = form.cleaned_data["facebook"]
        current_user_profile.save()
        info = True
        info_message = "Social Networks Updated !"
        parameters = {'info': info, 'info_message': info_message}
    else:
        error = True
        error_message = "Invalid Form Details"
        parameters = {'error': error, 'error_message': error_message}
    default_image = "/static/elearning_academy/img/default/user.jpg"
    parameters.update({'user_name': fullname,
                      'default_image': default_image,
                      'profile_exists': True})
    user_profile_dictionary = json.loads(current_user_profile.toJson())
    parameters.update(user_profile_dictionary)
    form = get_update_form(user)
    parameters.update(form)
    return render(request, 'user_profile/profile.html', parameters)


@login_required
def remove_user_work(request):
    """
        Remove a record for User Work Experience
    """
    user = request.user
    fullname = user.get_full_name()
    form = RemoveWorkform(request.POST)
    work_id = request.POST['work_id']
    work = Work.objects.filter(id=work_id)
    if (len(work) == 0) or (work[0].user != user):
        error = True
        error_message = "Work Experience not found in your records"
        parameters = {'error': error, 'error_message': error_message}
    else:
        work[0].delete()
        info = True
        info_message = "Work Experience removed"
        parameters = {'info': info, 'info_message': info_message}

    user_profile = UserProfile.objects.filter(user=user)
    if len(user_profile) != 0:
        profile_exists = True
        current_user_profile = user_profile[0]
        user_profile_dictionary = json.loads(current_user_profile.toJson())
        parameters.update(user_profile_dictionary)
    else:
        profile_exists = False
    default_image = "/static/elearning_academy/img/default/user.jpg"
    parameters.update({'user_name': fullname,
                      'default_image': default_image,
                      'profile_exists': profile_exists})
    form = get_update_form(user)
    parameters.update(form)
    return render(request, 'user_profile/profile.html', parameters)


@login_required
def add_user_work(request):
    """
        Add a record for User Work Experience
    """
    user = request.user
    fullname = user.get_full_name()
    form = AddWorkForm(request.POST)

    if (form.is_valid() and
        (form.cleaned_data["end_date"] is None or
            form.cleaned_data["end_date"] > form.cleaned_data["start_date"])):
        user_company = form.cleaned_data["company"]
        company = Company.objects.filter(company=user_company)
        if (len(company) == 0):
            company = Company()
            company.company = user_company
            company.save()
            user_company = company
        else:
            user_company = company[0]

        user_position = form.cleaned_data["position"]
        user_description = form.cleaned_data["description"]

        user_work = Work(user=user)
        user_work.company = user_company
        user_work.position = user_position
        user_work.description = user_description
        user_work.start_date = form.cleaned_data["start_date"]
        user_work.end_date = form.cleaned_data["end_date"]
        user_work.save()

        info = True
        info_message = "Added Work Experience !"
        parameters = {'info': info, 'info_message': info_message}
    else:
        error = True
        error_list = True
        error_message = []
        if form.cleaned_data["start_date"] is None:
            error_message.append("Start Date is required")
        if form.cleaned_data["company"] is None:
            error_message.append("Company is required")
        if form.cleaned_data["position"] is None:
            error_message.append("Position is required")
        if (form.cleaned_data["end_date"] is not None and
                (form.cleaned_data["end_date"] < form.cleaned_data["start_date"])):
            error_message.append("End Date has to be later than Start Date")
        parameters = {'error': error, 'error_list': error_list, 'error_message': error_message}

    user_profile = UserProfile.objects.filter(user=user)
    if len(user_profile) != 0:
        profile_exists = True
        current_user_profile = user_profile[0]
        user_profile_dictionary = json.loads(current_user_profile.toJson())
        parameters.update(user_profile_dictionary)
    else:
        profile_exists = False
    default_image = "/static/elearning_academy/img/default/user.jpg"
    parameters.update({'user_name': fullname,
                      'default_image': default_image,
                      'profile_exists': profile_exists})
    form = get_update_form(user)
    parameters.update(form)
    return render(request, 'user_profile/profile.html', parameters)


@login_required
def remove_user_education(request):
    """
        Remove a record for User Education Experience
    """
    user = request.user
    fullname = user.get_full_name()
    form = RemoveEducationForm(request.POST)
    education_id = request.POST['education_id']
    education = Education.objects.filter(id=education_id)
    if (len(education) == 0) or (education[0].user != user):
        error = True
        error_message = "Education instance not found in your records !"
        parameters = {'error': error, 'error_message': error_message}
    else:
        education[0].delete()
        info = True
        info_message = "Education record removed !"
        parameters = {'info': info, 'info_message': info_message}

    user_profile = UserProfile.objects.filter(user=user)
    if len(user_profile) != 0:
        profile_exists = True
        current_user_profile = user_profile[0]
        user_profile_dictionary = json.loads(current_user_profile.toJson())
        parameters.update(user_profile_dictionary)
    else:
        profile_exists = False
    default_image = "/static/elearning_academy/img/default/user.jpg"
    parameters.update({'user_name': fullname,
                      'default_image': default_image,
                      'profile_exists': profile_exists})
    form = get_update_form(user)
    parameters.update(form)
    return render(request, 'user_profile/profile.html', parameters)


@login_required
def add_user_education(request):
    """
        Add a record for User Education Experience
    """
    user = request.user
    fullname = user.get_full_name()
    form = AddEducationForm(request.POST)

    if (form.is_valid() and
        (form.cleaned_data["end_date"] is None or
            form.cleaned_data["end_date"] > form.cleaned_data["start_date"])):

        user_college = form.cleaned_data["college"]
        college = College.objects.filter(college=user_college)
        if len(college) != 0:
            user_college = college[0]
        else:
            college = College()
            college.college = user_college
            college.save()
            user_college = college

        user_major = form.cleaned_data["major"]
        major = Major.objects.filter(major=user_major)
        if len(major) != 0:
            user_major = major[0]
        else:
            major = Major()
            major.major = user_major
            major.save()
            user_major = major

        user_education = Education(user=user)
        user_education.college = user_college
        user_education.major = user_major
        user_education.degree = form.cleaned_data["degree"]
        user_education.start_date = form.cleaned_data["start_date"]
        user_education.end_date = form.cleaned_data["end_date"]
        user_education.save()

        info = True
        info_message = "Added Education Details !"
        parameters = {'info': info, 'info_message': info_message}
    else:
        error = True
        error_list = True
        error_message = []
        if form.cleaned_data["start_date"] is None:
            error_message.append("Start Date is required")
        if (form.cleaned_data["end_date"] is not None and
                (form.cleaned_data["end_date"] < form.cleaned_data["start_date"])):
            error_message.append("End Date has to be later than Start Date")
        parameters = {'error': error, 'error_list': error_list, 'error_message': error_message}

    user_profile = UserProfile.objects.filter(user=user)
    if len(user_profile) != 0:
        profile_exists = True
        current_user_profile = user_profile[0]
        user_profile_dictionary = json.loads(current_user_profile.toJson())
        parameters.update(user_profile_dictionary)
    else:
        profile_exists = False
    default_image = "/static/elearning_academy/img/default/user.jpg"
    parameters.update({'user_name': fullname,
                      'default_image': default_image,
                      'profile_exists': profile_exists})
    form = get_update_form(user)
    parameters.update(form)
    return render(request, 'user_profile/profile.html', parameters)


@login_required
def edit_user_personal_info(request):
    """
        Edit the User Personal Info in User Profile
    """
    user = request.user
    fullname = user.get_full_name()
    form = PersonalInfoForm(request.POST)

    user_profile = UserProfile.objects.filter(user=user)
    if len(user_profile) != 0:
        current_user_profile = user_profile[0]
    elif form.is_valid():
        current_user_profile = UserProfile(user=user)
        current_user_profile.generate_user_id()
        current_user_profile.save()

    if form.is_valid():
        current_user_profile.gender = form.cleaned_data["gender"]
        current_user_profile.dob = form.cleaned_data["dob"]
        current_user_profile.place_city = form.cleaned_data["city"]
        current_user_profile.place_state = form.cleaned_data["state"]
        current_user_profile.place_country = form.cleaned_data["country"]
        current_user_profile.save()
        info = True
        info_message = "Personal Information Updated !"
        parameters = {'info': info, 'info_message': info_message}
    else:
        error = True
        error_message = "Invalid Personal-Info Form Details"
        parameters = {'error': error, 'error_message': error_message}
    default_image = "/static/elearning_academy/img/default/user.jpg"
    parameters.update({'user_name': fullname,
                      'default_image': default_image,
                      'profile_exists': True})
    user_profile_dictionary = json.loads(current_user_profile.toJson())
    parameters.update(user_profile_dictionary)
    form = get_update_form(user)
    parameters.update(form)
    return render(request, 'user_profile/profile.html', parameters)


@login_required
def edit_user_intro(request):
    """
        Edit the User Intro in User Profile
    """
    user = request.user
    fullname = user.get_full_name()
    form = AboutForm(request.POST)

    user_profile = UserProfile.objects.filter(user=user)
    if len(user_profile) != 0:
        current_user_profile = user_profile[0]
    elif form.is_valid():
        current_user_profile = UserProfile(user=user)
        current_user_profile.generate_user_id()
        current_user_profile.save()

    if form.is_valid():
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.save()
        current_user_profile.about = form.cleaned_data["about"]
        current_user_profile.interests = form.cleaned_data["interests"]
        current_user_profile.save()
        info = True
        info_message = "Introduction Updated !"
        parameters = {'info':    info, 'info_message': info_message}
        print "success"
    else:
        error = True
        error_message = "Invalid Form Entry"
        parameters = {'error': error, 'error_message': error_message}
    default_image = "/static/elearning_academy/img/default/user.jpg"
    parameters.update({'user_name': fullname,
                      'default_image': default_image,
                      'profile_exists': True})
    user_profile_dictionary = json.loads(current_user_profile.toJson())
    parameters.update(user_profile_dictionary)
    form = get_update_form(user)
    parameters.update(form)
    return render(request, 'user_profile/profile.html', parameters)


def delete_image(url):
    """
        Delete the previous profile image of the user from media folder
    """
    try:
        os.remove(url)
    except WindowsError:
        print "%s does not exists" % url
    return True


@login_required
def edit_image(request):
    """
        Edit the profile image for a user profile
    """
    username = request.user.username
    user = User.objects.get(username=username)
    fullname = user.get_full_name()
    form = ImageForm(request.POST, request.FILES)

    user_profile = UserProfile.objects.filter(user=user)
    if len(user_profile) != 0:
        current_user_profile = user_profile[0]
    elif form.is_valid():
        current_user_profile = UserProfile(user=user)
        current_user_profile.generate_user_id()
        current_user_profile.save()

    if form.is_valid():
        photo = request.FILES["image"]
        if str(current_user_profile.photo) != "":
            delete_image(MEDIA_ROOT + str(user_profile[0].photo))
        current_user_profile.photo = photo
        current_user_profile.save()
        info = True
        info_message = "Image Succesfully Updated !"
        parameters = {'info': info, 'info_message': info_message}
    else:
        error = True
        error_message = "Please select a valid Image"
        parameters = {'error': error, 'error_message': error_message}

    default_image = "/static/elearning_academy/img/default/user.jpg"
    parameters.update({
        'user_name': fullname,
        'default_image': default_image,
        'profile_exists': True
    })
    user_profile_dictionary = json.loads(current_user_profile.toJson())
    parameters.update(user_profile_dictionary)
    form = get_update_form(user)
    parameters.update(form)
    return render(request, 'user_profile/profile.html', parameters)


@login_required
def all_data(request, key):
    """
        return a json of all colleges or major in the database
    """
    if key == "college":
        response_data = [c.college for c in College.objects.all()]
    elif key == "company":
        response_data = [c.company for c in Company.objects.all()]
    else:
        response_data = [m.major for m in Major.objects.all()]
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def view_settings(request):
    """
        Edit User contrib details for user
        Edit general preference on mails/ updates/ forums/ default mode
    """
    return render(request, 'user_profile/settings.html', {})


def switch_mode(request):
    """
        Switch the mode if its possible at this authorization
    """
    print "Switching Mode"
    if (request.method == 'POST'):
        new_mode = request.POST['new_mode']
        print new_mode
        if ('mode' in request.session.keys()):
            cur_mode = request.session['mode']
        else:
            request.session['mode'] = 'S'
            cur_mode = 'S'
        request.session['mode'] = new_mode
        print is_valid_mode(request)
        if (is_valid_mode(request)):
            return HttpResponse(json.dumps({}), content_type="application/json",
                                status=status.HTTP_200_OK)
        else:
            request.session['mode'] = cur_mode
            return HttpResponse(json.dumps({}), content_type="application/json",
                                status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse(json.dumps({}), content_type="application/json",
                            status=status.HTTP_400_BAD_REQUEST)
