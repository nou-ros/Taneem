from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer

# working with django group 
from django.contrib.auth.models import Group


# creating customer profile created signals
def customer_profile(sender, instance, created, **kwargs):
    if created:
        #assigning group while registering
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        # saving new user in the customer user model
        Customer.objects.create(
            user = instance,
            name = instance.username            
            )
        print('Profile created!')

post_save.connect(customer_profile, sender=User)