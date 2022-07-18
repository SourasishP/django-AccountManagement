from django.contrib import admin
from show_user_details.models import user
from show_user_details.models import management_user
from show_user_details.models import perform_user
from show_user_details.models import user_profile

class user_details(admin.ModelAdmin):
    list_display=('uname','email','pswd','status','user_type','verified')

class management_user_details(admin.ModelAdmin):
	list_display=('uname','acc_no','amt')

class perform_user_details(admin.ModelAdmin):
	list_display=('trn_id','from_acc','to_acc','amt','remarks','date')

class user_profile_details(admin.ModelAdmin):
	list_display=('uname','photo','occupation','dob')


admin.site.register(user,user_details)
admin.site.register(management_user,management_user_details)
admin.site.register(perform_user,perform_user_details)
admin.site.register(user_profile,user_profile_details)