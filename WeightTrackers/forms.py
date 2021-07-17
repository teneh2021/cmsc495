

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Activities,  Weight, Profile, AddWeight, WeightTracker
from bootstrap_modal_forms.forms import BSModalForm


# Create your forms here.

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class BSModalModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    pass



class WeightUpdateForm(BSModalModelForm):
	
	class Meta:
		model = AddWeight
		fields = ['add_weight']

class CreateUserForm(UserCreationForm):
	class Meta:
		model = WeightTracker
		fields = ['user', 'password1', 'password2',]



class ProfileForm(forms.ModelForm):
	#password = None
	class Meta:
		model = Profile
		fields = ['age', 'user_gender', 'height',
                    'user_photo',  'first_name', 'last_name', ]


class SettingsForm(forms.ModelForm):
	#password = None
	class Meta:
		model = Weight
		fields = ['account_type',  'target_weight', 'finish_date', ]


class AddActivity(BSModalModelForm):
	class Meta:
		model = Activities
		fields=['add_activity', 'activity_level']

	


