# This is your new models.py file
# Location: /MyCollegeProject/college_project/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# -----------------------------------------------------------------------------
# AUTHENTICATION
# -----------------------------------------------------------------------------

# We are creating a custom User model that has everything Django's
# default user has, but we're adding the "role" field.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    profile_image_url = models.CharField(max_length=500, blank=True, null=True)

# -----------------------------------------------------------------------------
# CORE ACADEMICS
# -----------------------------------------------------------------------------

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    head_of_department = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped'),
    )
    # This links this Student profile to our User model.
    # A User *is* a Student.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="students")
    year = models.IntegerField()
    semester = models.IntegerField()
    enrollment_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.student_id})"

class Faculty(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('retired', 'Retired'),
    )
    # A User *is* a Faculty member.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="faculty_profile")
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="faculty_members")
    designation = models.CharField(max_length=50, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.employee_id})"

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="courses")
    semester = models.IntegerField()
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CourseAssignment(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="course_assignments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="faculty_assignments")
    academic_year = models.CharField(max_length=10)
    semester = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty} -> {self.course} ({self.academic_year})"

class Timetable(models.Model):
    DAY_CHOICES = (
        (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
        (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="timetable_entries")
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name="timetable_entries")
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=10)
    semester = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name="attendance_marked")
    created_at = models.DateTimeField(auto_now_add=True)

# -----------------------------------------------------------------------------
# EXAMINATIONS
# -----------------------------------------------------------------------------

class Examination(models.Model):
    TYPE_CHOICES = (
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    )
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="examinations")
    exam_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    room = models.CharField(max_length=20, blank=True, null=True)
    max_marks = models.IntegerField(blank=True, null=True)
    academic_year = models.CharField(max_length=10)
    semester = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.course.name})"

class ExamResult(models.Model):
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="exam_results")
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# -----------------------------------------------------------------------------
# LIBRARY
# -----------------------------------------------------------------------------

class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    location = models.CharField(max_length=50, blank=True, null=True)
    publication_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BookIssue(models.Model):
    STATUS_CHOICES = (
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issues")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="book_issues")
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    fine = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')
    created_at = models.DateTimeField(auto_now_add=True)

# -----------------------------------------------------------------------------
# FEES
# -----------------------------------------------------------------------------

class FeeStructure(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="fee_structures")
    year = models.IntegerField()
    semester = models.IntegerField()
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lab_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hostel_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    misc_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    academic_year = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total fee
        self.total_fee = (self.tuition_fee + self.lab_fee + self.library_fee + 
                          self.hostel_fee + self.transport_fee + self.misc_fee)
        super().save(*args, **kwargs)

class FeePayment(models.Model):
    STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fee_payments")
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

# -----------------------------------------------------------------------------
# HOSTEL
# -----------------------------------------------------------------------------

class Hostel(models.Model):
    TYPE_CHOICES = ( ('boys', 'Boys'), ('girls', 'Girls') )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    total_rooms = models.IntegerField(blank=True, null=True)
    occupied_rooms = models.IntegerField(default=0)
    warden = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HostelRoom(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    )
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField(default=1)
    occupied_beds = models.IntegerField(default=0)
    rent = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

class HostelAllocation(models.Model):
    STATUS_CHOICES = ( ('active', 'Active'), ('checkout', 'Checkout') )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="hostel_allocation")
    room = models.ForeignKey(HostelRoom, on_delete=models.SET_NULL, null=True, related_name="allocations")
    allocation_date = models.DateField()
    checkout_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

# -----------------------------------------------------------------------------
# TRANSPORT
# -----------------------------------------------------------------------------

class TransportRoute(models.Model):
    route_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100, blank=True, null=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    distance = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fare = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    driver_name = models.CharField(max_length=100, blank=True, null=True)
    driver_contact = models.CharField(max_length=20, blank=True, null=True)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.route_name

class TransportAssignment(models.Model):
    STATUS_CHOICES = ( ('active', 'Active'), ('inactive', 'Inactive') )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="transport_assignment")
    route = models.ForeignKey(TransportRoute, on_delete=models.SET_NULL, null=True, related_name="assignments")
    assignment_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

# -----------------------------------------------------------------------------
# SPORTS
# -----------------------------------------------------------------------------

class SportsEquipment(models.Model):
    CONDITION_CHOICES = (
        ('excellent', 'Excellent'), ('good', 'Good'),
        ('fair', 'Fair'), ('poor', 'Poor')
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    total_quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    location = models.CharField(max_length=50, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SportsEquipmentIssue(models.Model):
    STATUS_CHOICES = ( ('issued', 'Issued'), ('returned', 'Returned'), ('lost', 'Lost') )
    equipment = models.ForeignKey(SportsEquipment, on_delete=models.CASCADE, related_name="issues")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sports_issues")
    issue_date = models.DateField()
    expected_return_date = models.DateField(blank=True, null=True)
    actual_return_date = models.DateField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    condition = models.CharField(max_length=10, choices=SportsEquipment.CONDITION_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')
    created_at = models.DateTimeField(auto_now_add=True)