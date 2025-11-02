# --- File: core/management/commands/seed_data.py ---
# This is the full and correct file (FIXED AGAIN)

import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from faker import Faker

# Import all our models
from core.models import User
from students.models import Department, Student
from faculty.models import Faculty
from courses.models import Course, CourseAssignment # <-- IMPORT CourseAssignment

# --- Settings ---
NUM_DEPARTMENTS = 10
NUM_FACULTY = 10
NUM_STUDENTS = 20 # Reduced to 50 in your last output, but let's go big
NUM_COURSES = 50
# --- End Settings ---

class Command(BaseCommand):
    help = 'Populates the database with a large set of fake data for testing and development.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--wipe',
            action='store_true',
            help='Wipes all existing data (Students, Faculty, Courses, Departments, non-superuser Users) before seeding.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR('Seed data command can only be run in DEBUG mode.'))
            return

        self.stdout.write(self.style.WARNING('Seeding database... Please wait.'))
        
        faker = Faker('en_IN') # Use Indian names and data

        if options['wipe']:
            self.stdout.write(self.style.WARNING('WIPING existing data (except superusers)...'))
            # Order of deletion matters
            CourseAssignment.objects.all().delete() # <-- WIPE ASSIGNMENTS
            Course.objects.all().delete()
            Student.objects.all().delete()
            Faculty.objects.all().delete()
            Department.objects.all().delete()
            User.objects.filter(is_superuser=False, is_staff=False).delete()

        # === 1. Create Superuser ===
        admin_user, created = User.objects.get_or_create(
            username='admin', 
            defaults={
                'email': 'admin@campusconnect.dev',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('adminpass123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: admin (Password: adminpass123)'))

        # === 2. Create Departments ===
        self.stdout.write('Creating Departments...')
        departments = []
        dept_names = [
            'Computer Science', 'Electronics Engineering', 'Mechanical Engineering', 
            'Civil Engineering', 'Chemical Engineering', 'Biotechnology', 
            'Physics', 'Mathematics', 'Chemistry', 'Humanities'
        ]
        dept_codes = ['CSE', 'ECE', 'ME', 'CE', 'CHE', 'BIO', 'PHY', 'MATH', 'CHEM', 'HUM']
        
        for i in range(len(dept_names)):
            dept, _ = Department.objects.get_or_create(
                code=dept_codes[i],
                defaults={
                    'name': dept_names[i],
                    'head_of_department': faker.name(),
                    'description': faker.paragraph(nb_sentences=3)
                }
            )
            departments.append(dept)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} Departments.'))

        # === 3. Create Faculty ===
        self.stdout.write('Creating Faculty...')
        faculty_users = []
        for i in range(NUM_FACULTY):
            first_name = faker.first_name()
            last_name = faker.last_name()
            username = f'f{faker.user_name()}{i}'
            email = f'{username}@campusconnect.dev'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'faculty'
                }
            )
            if created:
                user.set_password('faculty123')
                user.save()

            faculty, _ = Faculty.objects.get_or_create(
                user=user,
                defaults={
                    'employee_id': f'F{2020 + (i % 5)}{random.randint(100, 999)}',
                    'department': random.choice(departments),
                    'designation': random.choice(['Professor', 'Associate Professor', 'Assistant Professor']),
                    'joining_date': faker.date_of_birth(minimum_age=5, maximum_age=30),
                    'specialization': faker.job(),
                    'phone': faker.phone_number(),
                    'salary': random.randint(50000, 150000),
                    'qualification': random.choice(['Ph.D.', 'M.Tech', 'M.Sc']),
                    'status': 'active'
                }
            )
            faculty_users.append(faculty)

        self.stdout.write(self.style.SUCCESS(f'Created {len(faculty_users)} Faculty members.'))

        # === 4. Create Students ===
        self.stdout.write('Creating Students...')
        student_users = []
        for i in range(NUM_STUDENTS):
            # (Same as before, no changes needed)
            first_name = faker.first_name()
            last_name = faker.last_name()
            username = f's{faker.user_name()}{i}'
            email = f'{username}@campusconnect.dev'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'student'
                }
            )
            if created:
                user.set_password('student123')
                user.save()
            year = random.randint(1, 4)
            student, _ = Student.objects.get_or_create(
                user=user,
                defaults={
                    'student_id': f'S{2024 - year}{random.randint(1000, 9999)}',
                    'department': random.choice(departments),
                    'year': year,
                    'semester': (year * 2) - random.randint(0, 1),
                    'section': random.choice(['A', 'B', 'C']),
                    'enrollment_date': faker.date_of_birth(minimum_age=year, maximum_age=year),
                    'phone': faker.phone_number(),
                    'address': faker.address(),
                    'guardian_name': faker.name(),
                    'guardian_relation': random.choice(['Father', 'Mother', 'Guardian']),
                    'guardian_phone': faker.phone_number(),
                }
            )
            student_users.append(student)
            
        self.stdout.write(self.style.SUCCESS(f'Created {len(student_users)} Students.'))

        # === 5. Create Courses ===
        self.stdout.write('Creating Courses...')
        courses_created = []
        for i in range(NUM_COURSES):
            dept = random.choice(departments)
            year = random.randint(1, 4)
            
            course, _ = Course.objects.get_or_create(
                # --- FIXED: Use 'course_code' for uniqueness ---
                course_code=f'{dept.code}{year}{i:02d}',
                defaults={
                    'name': f'{dept.name} Course {i:02d}',
                    'department': dept,
                    'year': year,
                    'semester': (year * 2) - random.randint(0, 1),
                    'credits': random.choice([2, 3, 4]),
                    'description': faker.paragraph(nb_sentences=2),
                    'course_type': random.choice(['core', 'elective', 'lab']),
                    'lecture_hours': random.randint(2, 4),
                    # --- FIXED: Removed 'faculty' field ---
                }
            )
            courses_created.append(course)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(courses_created)} Courses.'))

        # === 6. Create Course Assignments (NEW STEP) ===
        self.stdout.write('Creating Course Assignments...')
        assignments = []
        for course in courses_created:
            # Assign one faculty member to each course for now
            faculty_member = random.choice(faculty_users)
            assignment, _ = CourseAssignment.objects.get_or_create(
                course=course,
                faculty=faculty_member,
                defaults={
                    'academic_year': '2024-2025',
                    'semester': course.semester
                }
            )
            assignments.append(assignment)

        self.stdout.write(self.style.SUCCESS(f'Created {len(assignments)} Course Assignments.'))
        self.stdout.write(self.style.SUCCESS(f'\n=== Database Seeding Complete! ==='))