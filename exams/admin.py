from django.contrib import admin
from .models import Exam, Result

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'exam_type', 'exam_date', 'max_marks')
    list_filter = ('exam_type', 'exam_date', 'course__department')
    search_fields = ('name', 'course__title', 'course__code')
    autocomplete_fields = ('course',)
    date_hierarchy = 'exam_date'

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained', 'grade', 'is_pass')
    list_filter = ('exam__course__department', 'exam__exam_type', 'is_pass')
    search_fields = (
        'student__user__username', 'student__student_id', 
        'exam__name', 'exam__course__title'
    )
    autocomplete_fields = ('student', 'exam')