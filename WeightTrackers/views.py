

from django.forms.utils import to_current_timezone
from .forms import *
import math
from django.db.models import F
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from bootstrap_modal_forms.generic import (BSModalCreateView)
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, request, response
from django.urls import reverse
from django.contrib.auth.models import User as user
from .models import Profile, Calculate, AddWeight, Activities, WeightTracker
from django.views.generic import  ListView
import random
# Create your views here.
from django.db.models import Window, F
from django.db.models.functions import Lead

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from random import randint
from django.utils import timezone




""" 
with tempfile.NamedTemporaryFile(delete=False) as output:
		output.write(result)
		output.flush()
		output = open(output.name, 'r')
		response.write(output)
"""


def generate_pdf(request):
	if request.user.is_authenticated:
		people = Calculate.objects.all().order_by('entry_date')
		html_string = render_to_string('WeightTrackers/generate_pdf.html', {'people': people})

		html = HTML(string=html_string)
		html.write_pdf(target='mypdf.pdf')

		fs = FileSystemStorage('.')
		with fs.open('mypdf.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
			return response
	return HttpResponse("Downloading is only for logged in user")

def test(request):
	people = Calculate.objects.all().order_by('entry_date')

	return render(request, 'WeightTrackers/generate_pdf.html', {'people': people})

def calc():
	calorie =0
	weight =0
	height=0
	for entry in Profile.objects.all():
		if entry.age is None:
			age=0
			height=0
		else:
			age = entry.age
			height = entry.height


	for entry in AddWeight.objects.all():
		if entry.add_weight is None:
			weight = 0
		else:
			weight = entry.add_weight
			

		
	if Profile.objects.filter(user_gender='Female'):
		bmr_female = 655 +(9.6 * weight * 0.454) + (1.8 * height * 2.54) - (4.7 * age) 
			
		if Activities.objects.order_by('-activity_level').filter(activity_level='Sedentary'):
			calorie = bmr_female * 1.2

		elif Activities.objects.order_by('-activity_level').filter(activity_level='Lightly active'):
			calorie = bmr_female * 1.375

		elif Activities.objects.order_by('-activity_level').filter(activity_level='Moderately active'):
			calorie = bmr_female * 1.55

		elif Activities.objects.order_by('-activity_level').filter(activity_level='Very active'):
			calorie = bmr_female * 1.725

		elif Activities.objects.order_by('-activity_level').filter(activity_level='Extra active'):
			calorie = bmr_female * 1.9
		
		return round(calorie, 2)

	elif Profile.objects.filter(user_gender='Male'):
		bmr_male = 66 + (13.7 * weight * 0.454 ) + (5 * height * 2.54) - (6.8 * age)
		if Activities.objects.order_by('-activity_level').filter(activity_level='Sedentary'):
			calorie = bmr_male * 1.2
			
		elif Activities.objects.order_by('-activity_level').filter(activity_level='Lightly active'):
			calorie = bmr_male * 1.375

		elif Activities.objects.order_by('-activity_level').filter(activity_level='Moderately active'):
			calorie = bmr_male * 1.55

		elif Activities.objects.order_by('-activity_level').filter(activity_level='Very active'):
			calorie = bmr_male * 1.725

		elif Activities.objects.order_by('-activity_level').filter(activity_level='Extra active'):
			calorie = bmr_male * 1.9
		return round(calorie, 2)
	else:
		return round(calorie,2)


def bmi_calc():
	height=0
	weight =0
	for entry in AddWeight.objects.all():
		weight =  entry.add_weight
		
	for entry in Profile.objects.all():
		height = entry.height
	if  height != 0:
		bmi = weight * 0.454 /(height * height * 0.0254 * 0.0254)
	else:
		bmi =0
	return round(bmi, 2)

def weight_diff():
	weight_list =[]
	
	for entry in AddWeight.objects.all():
		weight_list.append(entry.add_weight)
	if len(weight_list)>=2:
		weight_diff=weight_list[-1] - weight_list[-2]
	elif len(weight_list)<=1:
		weight_diff=0

	return abs(weight_diff)
""""**************************************************************Global variables here *********************************************************"""

class AllInOne():

	def user_photo(self):
		entry = Profile.objects.values_list('user_photo')
		if len(entry) !=0:
			user_photo = entry[0]
		else:
			user_photo ="No user photo"
		return user_photo

	def total_loss_gain(self):
		list_item = AddWeight.objects.values_list('add_weight', flat=True)
		listed = list(list_item)

		total_loss = 0
		#entry = AddWeight.objects.values_list('add_weight', flat=True)
		if len(listed) != 0:
			first_item = listed[0]
			last_item = listed[-1]
			total_loss = abs(first_item - last_item)
		else:
			total_loss =0
		return total_loss
	
	def time_elapsed(self):
		for ent in WeightTracker.objects.all():
			dated = ent.date_created
		time_elaps= timezone.now() - dated
		return time_elaps.days

	def health_tip(self):
		line = 0
		linee = []
		fs = FileSystemStorage('.')
		fact_file = fs.open('health_facts.txt', 'r')
		for lines in fact_file:
			lengh = lines.split('\n')
			linee.append(lengh)
			line += 1
		randa = randint(0, line)
		return linee[randa][0]
		

class WeightCreateView(BSModalCreateView):
	template_name = 'WeightTrackers/book.html'
	form_class = WeightUpdateForm

	def form_valid(self, form):
		add_calorie =AddWeight.objects.get_or_create(add_weight=form.cleaned_data['add_weight'],  topic=self.request.user)
		add_calorise = Calculate.objects.get_or_create(
			weight=form.cleaned_data['add_weight'], bmi=bmi_calc(), calorie=calc(), weight_difference=weight_diff(), topic=self.request.user)
		
		return redirect('dashboard')



class AddActivityView(BSModalCreateView):
	template_name = 'WeightTrackers/book.html'
	form_class = AddActivity

	def form_valid(self, form):
		activity = form.cleaned_data.get('add_activity')
		level = form.cleaned_data.get('activity_level')
		activities=Activities.objects.get_or_create(topic=self.request.user, add_activity=activity, activity_level=level)
		
		return redirect('target')


@login_required
def user_home(request):
	all_func = AllInOne()
	weights =AddWeight.objects.values_list('add_weight', flat=True)
	weight_list= list(weights)
	if len(weight_list) !=0:
		first_wt = weight_list[0]
		last_wt = weight_list[-1]
	else:
		first_wt = "Weight not added yet"
		last_wt = "Weight not added yet"
	activity= Activities.objects.values_list('add_activity', flat=True)
	activity_list= list(activity)
	if len(activity_list) !=0:
		activated = activity_list[-1]
	else:
		activated = "No activities added"

	context={'user_pict': all_func.user_photo(), 'time_elapse': all_func.time_elapsed(), 'add_activity': activated, 'health_tip':all_func.health_tip(),
	 'first_item': first_wt, 'last_item': last_wt, 'bmi': bmi_calc(), 'total_loss': all_func.total_loss_gain() }
		
	return render(request, 'WeightTrackers/home.html', context)


def user_login(request):
	
	if request.user.is_authenticated:
		return redirect('home')

	if request.method == "POST":

		USER = request.POST.get('username')
		PASSWORD = request.POST.get('password')

		user = authenticate(request, username=USER, password = PASSWORD)
		if user is not None:
			login(request, user)
			
			return render(request=request, template_name='WeightTrackers/home.html')
		else:
			messages.info(request, 'Username OR Password is incorrect')
		
	return render(request=request, template_name='WeightTrackers/login.html')



@login_required
def user_logout(request):
	logout(request)
	return redirect('/login')


def user_register(request):
	if request.user.is_authenticated:
		return redirect('/home')
	else:
		form = UserCreationForm()
		if request.method == 'POST':
			form = UserCreationForm(request.POST)
			if form.is_valid():
			
				form.save(commit=True)
				
				
				user = form.cleaned_data.get('username')
				username=User.objects.get(username=user)
				weighttracker = WeightTracker.objects.create(user=username)
				messages.success(request, 'Account was created for ' + user)
				
				return redirect('/login')		
	
		context = {'form':form}
		return render(request, 'WeightTrackers/register.html', context)


	
def editProfile(request):
	
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance=request.user)

		if form.is_valid():

		
			age = form.cleaned_data.get('age')
			user_gender = form.cleaned_data.get('user_gender')
			height = form.cleaned_data.get('height')
			user_photo = form.cleaned_data.get('user_photo')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			user = request.user
			q = Profile.objects.all()
			q.delete()
			profile_setting = Profile.objects.update_or_create(user=user, first_name=first_name, last_name=last_name,
                                                      age=age, user_gender=user_gender, height=height, user_photo=user_photo)
			form.save()	
			return redirect('/home')
		else:
			return HttpResponse("Entry not valid")
	else:
		
		form = ProfileForm(instance=request.user)
		
		args = {'form': form}
		return render(request, 'WeightTrackers/profile.html', args)


def user_settings(request):
	
	#form = SettingsForm()
	#form = ProfileForm()

	if request.method == 'POST':
		form = SettingsForm(request.POST)
		

		if form.is_valid():
			q = Weight.objects.all()
			q.delete()
			weight_setting = form.save(commit=False)
			#weight_setting.topic = request.user
			weight_setting.save()
			request.user.weights.add(weight_setting)

			#calc()
			#bmi_calc()
			#add_calorie = Calculate.objects.get_or_create(weight_difference=weight_diff(),weight=weight, calorie=calc(), bmi=bmi_calc(), topic=request.user)
			
			return redirect('/home')

		else:
			print("Data is not valid")
	else:
		form = SettingsForm(request.POST)
		my_dict = {'form': form}
		return render(request, 'WeightTrackers/user_settings.html', context=my_dict)





class LineChartJSONView(BaseLineChartView):
	weighted =[]
	dated =[]

	def get_labels(self):
		"""Return 7 labels for the x-axis."""
		return ['Sunday', 'Monday', 'Tuesday', 'Wed', 'Thur', 'Fri', 'Sat',]


	def get_providers(self):

		"""Return names of datasets."""
		return ["Central", "Eastside", "Westside"]

	def get_data(self):
		"""Return 3 datasets to plot."""

		return [[75, 44, 92, 11, 44, 95, 35],
				[self.weighted],]
				#[87, 21, 94, 3, 90, 13, 65]]
				


line_chart = TemplateView.as_view(template_name='dashboard.html')
line_chart_json = LineChartJSONView.as_view()


def dashboard(request):

	calculations =[]
	for entry in Calculate.objects.all():
		calculations.append(entry)
	my_dict = {'calc': calculations[-5:]}
	calculations =0
	return render(request, 'WeightTrackers/dashboard.html', context=my_dict)


def welcome(request):
    my_dict = {'insert_me': "Hello I amm from views.py!"}
    return render(request, 'WeightTrackers/welcome.html', context=my_dict)


def target(request):
	all_func=AllInOne()
	weights = AddWeight.objects.values_list('add_weight', flat=True)
	weight_list = list(weights)
	if len(weight_list) != 0:
		first_wt = weight_list[0]
		last_wt = weight_list[-1]
	else:
		first_wt = 0
		last_wt = 0

	target_date1 = Weight.objects.values_list('finish_date', flat=True)
	target_date = list(target_date1)
	if len(target_date) !=0:
		target_date2 = target_date[-1]
		for entry in Weight.objects.all():
			finish_wt=entry.target_weight
	else:
		target_date2 ="Not set yet"
		finish_wt =0
	weight_diff = first_wt - finish_wt
	wt_quotient= 100/weight_diff
	current_wt_diff= first_wt -last_wt
	slide_value = current_wt_diff * wt_quotient
	""" target date section"""
	for ent in WeightTracker.objects.all():
		dated = ent.date_created

	""" Bmi section"""
	heihgt_list = Profile.objects.values_list('height', flat=True)
	if len(heihgt_list) !=0:
		height = list(heihgt_list)[-1]
	else:
		height =1
	target_bmi = finish_wt * 0.454 / (height * height * 0.0254 * 0.0254)
	initial_bmi_list = Calculate.objects.values_list('bmi', flat=True)
	if len(initial_bmi_list) !=0:
		initial_bmi = initial_bmi_list[0]
	else:
		initial_bmi = 0

	bmi_diff = abs(initial_bmi - target_bmi)
	bmi_quotient = 100/bmi_diff

	bmi_progress =bmi_quotient * abs(target_bmi - bmi_calc() )
	print(bmi_progress)

	activity =None
	for entry in Activities.objects.all():
		activity = entry.add_activity
	my_dict = {'first_item': first_wt, 'last_item': last_wt, 'slide_value': slide_value, 'initial_bmi': initial_bmi,
	'time_elapse': all_func.time_elapsed(), 'target_date': target_date2, 'start_date': dated.date, 'target_bmi': target_bmi,
	 'total_loss': all_func.total_loss_gain(), 'activity': activity, 'finish_wt': finish_wt, 'bmi_progress': bmi_progress}
	return render(request, 'WeightTrackers/target.html', context=my_dict)


def bmi(request):
	#bmi_list = Calculate.objects.latest('bmi')
	
	weight_list =0
	bmi_list=0
	bmi_value = Calculate.objects.values_list('bmi', flat=True)
	for entry in Calculate.objects.all():
		bmi_list =entry.bmi
		
	
	for entry in AddWeight.objects.all():
		weight_list = entry.add_weight
	#weight_list=Weight.objects.latest('add_weight')
	statuses =['Underweight', 'Normal weight', 'Overweight', 'Obese']
	status=''
	
	if bmi_list <= 18.5:
		status = statuses[0]
	elif bmi_list >18.5 and bmi_list <= 24.9:
		status = statuses[1]
	elif bmi_list > 24.9 and bmi_list<=31:
		status= statuses[2]
	elif bmi_list >31:
		status =statuses[3]
	clock_bmi = bmi_list * 4.5
	return render(request, 'WeightTrackers/bmi.html', {'clock_bmi': clock_bmi, 'bmi': bmi_list, 'weight':weight_list, 'status': status})




"""  
#from weasyprint import HTML

def html_to_pdf_view(request):
	paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
	html_string = render_to_string(
		'WeightTrackers/dashboard.html', {'paragraphs': paragraphs})

	html = HTML(string=html_string)
	html.write_pdf(target='/tmp/mypdf.pdf')

	fs = FileSystemStorage('/tmp')
	with fs.open('mypdf.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
		return response
	#return response




q = AddWeight.objects.annotate(
    next_val=Window( expression=Lead('add_weight', offset=1, default=0),
        
    ),
    difference=F('add_weight')-F('next_val'),
)


if q.difference=='':
	AddWeight.difference =0
	print(q.difference)
else:
	print(q.difference)

	age_list=Profile.objects.order_by('-age').values_list('age', flat=True)	
	if len(age_list) !=0:
		age =  age_list[0]
	else:
		age=0
	height_list = Profile.objects.order_by('-height').values_list('height', flat=True)
	if len(height_list) !=0:
		height=height_list[0]
	else:
		height=0

	weight_list = AddWeight.objects.order_by('-add_weight').values_list('add_weight', flat=True)
	if len(weight_list) !=0:
		weight= weight_list[0]
	else:
		weight = 0
"""

"""

class BoardListView(ListView):
    model = Calculate
    context_object_name = 'calc'
    template_name = 'dashboard.html'



def user_image(request):
  
    if request.method == 'GET':
  
        # getting all the objects of hotel.
        user_pict = Profile.objects.all() 
        return render(request, 'WeightTrackers/home.html',  {'user_pict' : user_pict})


def testing(request):
	bmi_list =  Calculate.objects.latest()
	print(bmi_list)
	return render(request, 'WeightTrackers/testing.html', {})

def profile(request):
	
	
	form = ProfileForm()
	
	if request.method == 'POST':
		
		form = ProfileForm(request.POST, request.FILES)

		if form.is_valid():
			weight_setting=form.save(commit=False)
			weight_setting.user = request.user
			weight_setting.save()
			calc()
			bmi_calc()
			add_calorie = Calculate.objects.get_or_create(weight_difference=weight_diff(),
				calorie=calc(), bmi=bmi_calc(), topic=request.user)

			return redirect('/home')

		else:
			print("Data is not valid")
	
	my_dict = {'form': form}
	return render(request, 'WeightTrackers/profile.html', context=my_dict)

#add_calorie = Calculate.objects.get_or_create(calorie=calc())
#add_bmi = Calculate.objects.get_or_create(bmi=bmi_calc())
			
posting = Weight.objects.order_by("-add_weight")
last_wt = posting[0]
print(last_wt)
print(posting)

cc = Calculate()
print(cc.bmi)
for entry in Profile.objects.all():
	age = entry.age

second_last = posting[1]
print(second_last)
"""
