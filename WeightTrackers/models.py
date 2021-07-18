
from django.db.models import ExpressionWrapper, DecimalField
from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.expressions import OrderBy

# Create your models here.
GENDER = (
	('Male', 'Male'),
	('Female', 'Female'),)

ACCOUNT_TYPE = (
	('Weight Gain', 'weight gain'),
	('Weight Loss', 'weight loss'),
)

message ="Sedentary: Little or no exercise.  \nLightly active: Light exercise/sports 1-3 days/week. \nModerately active: Moderate exercise/sports 3-5 days/week.\nVery active: Hard exercise/sports 6-7 days/week.\nExtra active: Very hard exercise/sports and physical job"

ACTIVITY_LEVEL = (
    ('Sedentary', 'Sedentary'),
     ('Lightly active', 'Lightly active'),
      ('Moderately active', 'Moderately active'),
       ('Very active', 'Very active'),
        ('Extra active', 'Extra active'),
)

class WeightTracker(models.Model):
    
    #username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='WeightTracker', null=True)
    user = models.OneToOneField(User, null=True, related_name='weighttracker', on_delete=models.CASCADE) 
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Profile(models.Model):
    user = models.ForeignKey(User, null=True, related_name='profiles', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256, null=True)
    last_name = models.CharField(max_length=256, null=True)
    age = models.PositiveIntegerField()
    user_gender =models.CharField(max_length=15, choices=GENDER,  blank=True,
        default='Male',
        verbose_name='Gender')
 
    height = models.FloatField(max_length=20, default=0, verbose_name='Enter your height')
    user_photo = models.ImageField(upload_to='WeightTrackers/media/',  blank=True)

    def __str__(self):
        return str(self.user)

class AddWeight(models.Model):
    topic =models.ForeignKey(User, null=True, related_name="add_weight", on_delete=models.CASCADE)
    add_weight=models.FloatField(max_length=20, default=0, verbose_name='Enter your weight:')

    def __str__(self):
        return str(self.add_weight)

class Weight(models.Model):
    topic = models.ForeignKey(User, null=True, related_name='weights', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE,
                                    default='Weight Loss',
                                    verbose_name='Account Type')   
    
    target_weight = models.FloatField(max_length=20, default=0,  verbose_name='Enter your target weight') 
    finish_date = models.DateField(null=True)
    def __str__(self):
        return str(self.topic)



class Activities(models.Model):
    topic = models.ForeignKey(User,  related_name='activities', on_delete=models.CASCADE)
    add_activity = models.TextField( blank=True)
    activity_level =models.CharField(max_length=100, choices=ACTIVITY_LEVEL,  blank=True,
        default='Lightly active',
        verbose_name='Activity intensity',
        help_text=message)

    def __str__(self):
        return str(self.topic)


class Calculate(models.Model):
    topic = models.ForeignKey(
        User, null=True, related_name='calculates', on_delete=models.CASCADE)
    
    bmi = models.FloatField(max_length=20, default=0,
                            verbose_name='Body Mass Index')
    calorie = models.FloatField(
        max_length=20, default=0,  verbose_name='Calorie')
    entry_date = models.DateField(auto_now_add=True, null=True)
    weight = models.FloatField(max_length=20, default=0,
                            verbose_name='Weight')
    weight_difference = models.FloatField(
        max_length=20, default=0,  verbose_name='Weight Loss')

    def __str__(self):
        return str(self.topic)

 
"""
    def bmi_func(self):
        return self.bmi

    def calorie_func(self):
        return self.calorie

    def weight_diff(self):
        self.weight_difference= AddWeight.objects.annotate(
            F(OrderBy('-add_weight')[0]) - F(OrderBy('-add_weight')[1]))
    
        #return str(weight_difference)





   bmi = ExpressionWrapper(
    F('start_weight') * 0.454 / (F('height') * F('height') * 0.0254 * 0.0254), output_field=DecimalField()
)
Profile.objects.all().annotate(
    bmi=ExpressionWrapper(
        F('start_weight') * 0.454 / (F('height') * F('height') * 0.0254 * 0.0254), output_field=DecimalField()
    )
)

profile = models.ForeignKey(
        Profile, related_name='calculates', on_delete=models.CASCADE)
    weight = models.ForeignKey(
        Weight, related_name='calculates', on_delete=models.CASCADE)
    activities = models.ForeignKey(
        Activities, related_name='calculates', on_delete=models.CASCADE)

GENDER = (
	('m', 'Male'),
	('f', 'Female'),)

ACCOUNT_TYPE = (
	('wg', 'Weight Gain'),
	('wl', 'Weight Loss'),
)



bmi = Weight.current_weight*0.454/(Weight.height * Weight.height * 0.254 * 0.254)
    calorie_male = models.DecimalField(max_length=40)
    calorie_female = models.DecimalField(max_length=40)
    bmr_female = (10 * Weight.age) + (6.25* Weight.height) - (5* Weight.age) - 161
    bmr_male = (10 * Weight.age) + (6.25 * Weight.height) - (5 * Weight.age) - 161
BMR equation can be used to calculate calorie using the activity type
For men: BMR = 10 x weight (kg) + 6.25 x height (cm) – 5 x age (years) + 5

For women: BMR = 10 x weight (kg) + 6.25 x height (cm) – 5 x age (years) – 161
Activity type:
Sedentary (little or no exercise) : Calorie-Calculation = BMR x 1.2
Lightly active (light exercise/sports 1-3 days/week) : Calorie-Calculation = BMR x 1.375
Moderately active (moderate exercise/sports 3-5 days/week) : Calorie-Calculation = BMR x 1.55
Very active (hard exercise/sports 6-7 days a week) : Calorie-Calculation = BMR x 1.725
extra active (very hard exercise/sports & a physical job) : Calorie-Calculation = BMR x 1.9

"""
