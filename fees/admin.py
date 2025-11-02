from django.contrib import admin
from .models import FeeStructure, FeePayment

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('department', 'year', 'total_fee', 'tuition_fee', 'hostel_fee', 'transport_fee')
    list_filter = ('department', 'year')

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'semester', 'total_amount', 'amount_paid', 'balance_due', 'status')
    list_filter = ('status', 'academic_year', 'semester', 'student__department')
    search_fields = ('student__user__username', 'student__student_id', 'transaction_id')
    autocomplete_fields = ('student',)