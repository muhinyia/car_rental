from django.contrib import admin
from .models import Reservation, Car, Station, Contact

from django.contrib.auth.models import User, Group


class StationAdmin(admin.ModelAdmin):
    list_display = ['name',  'county', 'town', 'mobile', 'manager']
    list_display_links = ['name']
    list_filter = ['county', 'town']


admin.site.register(Station, StationAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['customer', 'email', 'message']

    list_filter = ['customer']

    def has_add_permission(self, request):
        return False

admin.site.register(Contact, ContactAdmin)


class CarAdmin(admin.ModelAdmin):
    list_display = ['name',  'Reg_No', 'model',
                    'available', 'fee', 'fine_rate', 'description']
    list_display_links = ['name']
    list_filter = ['name', 'model', 'fee']


admin.site.register(Car, CarAdmin)


class ReservationAdmin(admin.ModelAdmin):

    list_display = ['car', 'station', 'pick_date', 'return_date',
                    'duration',  'customer', 'customer_phone', 'id_number']

    list_filter = ['station', 'pick_date',
                   'return_date', 'has_returned']

    def has_add_permission(self, request):
        return False


admin.site.register(Reservation, ReservationAdmin)


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name',
                    'last_name', 'is_active', 'last_login']

    readonly_fields = ['email', 'first_name',
                       'last_name', 'is_active', 'last_login']

    def has_add_permission(self, request):
        return False


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)
