import csv
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# from .models import Profile

User = get_user_model()

@admin.action(description="Export selected users to CSV")
def export_users_csv(modeladmin, request, queryset):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Username",
        "Email",
        "Location",
        "Birth Date",
        "Permanent Address"
        "Phone",
        "Qualification",
        "Gender",
    ])

    for user in queryset:

        # try:
        #     profile = user.profile
        # except Profile.DoesNotExist:
        #     profile = None

        writer.writerow([
            user.username,
            user.email,
            user.location,
            user.birth_date,
            user.permanent,
            user.pno,
            user.qualification,
            user.gender,
        ])

    return response


# class ProfileInline(admin.StackedInline):
#     model = 
#     extra = 0


class CustomUserAdmin(UserAdmin):
    # inlines = [ProfileInline]
    actions = [export_users_csv]


# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)