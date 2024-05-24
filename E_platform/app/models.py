from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from datetime import time


class CustomeUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_type_choices = ((1, 'ADMIN'),
                         (2, 'STUDENT'),
                         (3, 'COURSE PROVIDER'))
    user_type = models.IntegerField(choices=user_type_choices, default=1)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Course(models.Model):
    TECH_COURSE = 'Tech Courses'
    CBSE_COURSE = 'CBSE Courses'
    CATEGORY_CHOICES = [
        (TECH_COURSE, 'Tech Courses'),
        (CBSE_COURSE, 'CBSE Courses'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    what_you_will_learn = models.TextField(null=True, blank=True, verbose_name="What You Will Learn")
    this_course_includes = models.TextField(null=True, blank=True, verbose_name="This Course Includes")

    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default=TECH_COURSE)
    image = models.ImageField(upload_to='staticfiles/course_images/', null=True, blank=True)
    demo_video = models.FileField(upload_to='staticfiles/demo_videos/', null=True, blank=True)

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(CustomeUser, on_delete=models.CASCADE)
    Full_Name = models.CharField(max_length=20, null=True, blank=True)
    Mobile_no = models.CharField(max_length=10, null=True, blank=True)
    EmailID = models.EmailField(max_length=255, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    Gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )
    Gender = models.CharField(max_length=10, choices=Gender_choices, default='M')
    cart = models.ManyToManyField('Course', related_name='students_in_cart')
    wishlist = models.ManyToManyField('Course', related_name='students_in_wishlist')

    def __str__(self) -> str:
        return self.Full_Name

class Week(models.Model):
    course = models.ForeignKey(Course, related_name='weeks', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Week {self.number}: {self.title}"


class Topic(models.Model):
    week = models.ForeignKey(Week, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='staticfiles/topic_videos/', null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)
    watched_by_users = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return self.title

    def has_video(self):
        return bool(self.video_file or self.video_link)

    def get_video_url(self):
        if self.video_file:
            return self.video_file.url
        elif self.video_link:
            return self.video_link
        else:
            return None


class Quiz(models.Model):
    course = models.ForeignKey(Course, related_name='quizzes', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    weight = models.FloatField(default=0)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(default=timezone.now)
    time_limit = models.TimeField(default=time(0, 30))


    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz_questions', on_delete=models.CASCADE)
    question_no = models.IntegerField()
    question_text = models.TextField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(
        max_length=2,
        choices=[
            ('1', 'Option 1'),
            ('2', 'Option 2'),
            ('3', 'Option 3'),
            ('4', 'Option 4')
        ]
    )
    reason = models.TextField()

    def __str__(self):
        return f"{self.quiz.course} - {self.quiz.topic}"  
    
class QuizResult(models.Model):
    student = models.ForeignKey(Student, related_name='quiz_results', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='results', on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.quiz.title} - {self.score}/{self.total_questions}"
    
class SelectedAnswer(models.Model):
    student = models.ForeignKey(Student, related_name='selected_answers', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='selected_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, related_name='selected_answers', on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.user.username} - {self.quiz.title} - Question {self.question.question_no} - Option {self.selected_option}"

class StudentCourseProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_weeks = models.ManyToManyField(Week, blank=True)

class Certificate(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completion_date = models.DateTimeField(auto_now_add=True)
    certificate_image = models.ImageField(upload_to='staticfiles/certificates/')

    def __str__(self):
        return f"{self.user.Full_Name}'s Certificate for {self.course.title}"
    
class Grade(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.certificate.course} - {self.grade}"

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.user} enrolled in {self.course.title}"


class Mentorship(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    reason = models.TextField()
    phone_number = models.CharField(max_length=15)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Assuming each mentorship is associated with a course
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mentorship for {self.user.username}"


class QuestionPaper(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    grade = models.IntegerField(default=00)
    subject = models.CharField(max_length=100)
    file = models.FileField(upload_to='question_papers/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Post(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)


class Ticket(models.Model):
    REASON_CHOICES = [
        ('Payment Methods', 'Payment Methods'),
        ('Refund a Course', 'Refund a Course'),
        ('Troubleshoot Payment Failure', 'Troubleshoot Payment Failure'),
        ('Download Course Resources', 'Download Course Resources'),
        ('Enrollment', 'Enrollment'),
        ('Grades & Assignments', 'Grades & Assignments'),
        ('Video Library', 'Video Library'),
        ('Trust & Safety', 'Trust & Safety'),
        ('Find a missing course', 'Find a missing course'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    description = models.TextField()
    attachment = models.FileField(upload_to='staticfiles/tickets/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Open')

    def __str__(self):
        return f"Ticket #{self.id} - {self.user.email}"



class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    language = models.CharField(max_length=50, blank=True)
    linkedin_profile = models.URLField(blank=True)
    twitter_profile = models.URLField(blank=True)
    facebook_profile = models.URLField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class WorkExperience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

class PrivacySettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    show_profile_to_logged_in_users = models.BooleanField(default=True)
    show_courses_on_profile = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Privacy Settings"

class NotificationSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    promotion = models.BooleanField(default=True)
    helpful_resources = models.BooleanField(default=True)
    no_promotional_email = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Notification Settings"

class Referral(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    friend_email = models.EmailField()
    date_referred = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} referred {self.friend_email}"



class PaymentHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50)
    receipt_invoice = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.course_title} - {self.date}"


class Note(models.Model):
    course = models.ForeignKey(Course, related_name='notes', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='notes', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Note by {self.student.user.email} on {self.course.title}"