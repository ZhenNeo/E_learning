from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import *
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect
from .models import Course, Enrollment, QuestionPaper
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, FileResponse, HttpResponse
from django.http import JsonResponse
from .models import Post, Comment


# Create your views here.

# ---------------------------------------------------------------------------
# Login view
# ---------------------------------------------------------------------------
def do_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                user_type = user.user_type
                if user_type == 1:  # Assuming user_type is an integer field
                    return redirect('admin')
                elif user_type == 2:
                    return redirect('course_catalog')
                elif user_type == 3:
                    return HttpResponse('course provider')
                else:
                    messages.error(request, "Invalid Login!")
            else:
                messages.error(request, "Invalid Login!")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def generate_otp():
    return random.randint(100000, 999999)


def send_otp(email, otp):
    send_mail(
        'Email Verification OTP',
        f'Your OTP is: {otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def student_signup(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['EmailID']

            # Check if the email already exists
            if get_user_model().objects.filter(email=user_email).exists():
                messages.error(request, 'This email is already in use.')
                return redirect('student-signup')  # Redirect back to the signup page

            # Create a new user instance
            user = get_user_model().objects.create_user(
                email=user_email,
                password=form.cleaned_data['password1'],
                username=user_email,  # You can set username as email if you want
                user_type=2
            )
            # Generate a random OTP and send it to the user's email
            otp = generate_otp()

            # Send the OTP to the user's email
            send_otp(user_email, otp)

            # Save the OTP in the session
            request.session['otp'] = otp
            request.session['email'] = user_email

            return redirect('verify_otp')
    else:
        form = AdminForm()

    return render(request, 'student_signup.html', {'form': form})


def logout_user(request):
    return redirect('login')


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        if entered_otp == str(stored_otp):
            # OTP verification successful
            email = request.session.get('email')
            Full_Name = request.POST.get('Full_Name')

            # Create a student profile
            user = get_user_model().objects.get(email=email)
            student_profile = Student.objects.create(user=user,
                                                     Full_Name=user.email)
            # Redirect to a success page
            return redirect('course_catalog')

    # OTP verification failed or GET request
    return render(request, 'verify_otp.html')


def course_catalog(request):
    courses = Course.objects.all()
    return render(request, 'course_catalog.html', {'courses': courses})


def career_roadmap(request):
    courses = Course.objects.all()
    return render(request, 'career_roadmap.html', {'courses': courses})


def view_course_details(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'view_course_details.html', {'course': course})


def start_course(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'start_course.html', {'course': course})


@login_required
def enroll_course(request, course_id):
    if request.method == 'POST':
        # Create a new enrollment record for the current user and course
        Enrollment.objects.create(course_id=course_id, user=request.user)
        # Redirect to the enrolled course page
        return redirect('enrolled_course')
    else:
        # If the request method is not POST, redirect to the course details page
        return redirect('view_course_details', course_id=course_id)


def course_payment(request, course_id):
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['course_id'] = course_id
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request, 'course_payment.html', context)


@login_required
def enrolled_course(request):
    try:
        # Retrieve the Admin instance associated with the current user
        admin_user = Student.objects.get(user=request.user)
        # Retrieve enrolled courses for the admin user
        enrolled_courses = Enrollment.objects.filter(user=admin_user)
    except Student.DoesNotExist:
        # Handle the case where the user is not an admin
        enrolled_courses = []

    return render(request, 'enrolled_course.html', {'enrolled_courses': enrolled_courses})


def previous_question_papers(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    question_paper = QuestionPaper.objects.filter(course=course).first()

    if question_paper:
        # Assuming there's only one question paper per course for simplicity
        file_path = question_paper.file.path
        # Open the file and serve it as a download response
        response = FileResponse(open(file_path, 'rb'))
        # Set the content type header to force the browser to download the file
        response['Content-Disposition'] = f'attachment; filename="{question_paper.title}.pdf"'
        return response
    else:
        # Handle the case where no question paper is found
        return HttpResponse("No question paper found for this course.", status=404)


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def homepage(request):
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'mentorship_page.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()


@login_required
def community_platform(request):
    # Retrieve all posts for display
    posts = Post.objects.all()
    return render(request, 'community_platform.html', {'posts': posts})


@login_required
def add_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user.student  # Get the Student instance associated with the logged-in user
        post = Post.objects.create(user=user, content=content)
        return redirect('community_platform')
    return render(request, 'add_post.html')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user.student  # Get the Student instance associated with the logged-in user
        comment = Comment.objects.create(post=post, user=user, content=content)
        return redirect('community_platform')
    return render(request, 'add_comment.html', {'post': post})


def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.likes += 1
    post.save()
    return JsonResponse({'likes': post.likes})


def dislike_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.dislikes += 1
    post.save()
    return JsonResponse({'dislikes': post.dislikes})


def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.likes += 1
    comment.save()
    return JsonResponse({'likes': comment.likes})


def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.dislikes += 1
    comment.save()
    return JsonResponse({'dislikes': comment.dislikes})




@login_required
def view_cart(request):
    cart_courses = request.user.student.cart.all()
    return render(request, 'view_cart.html', {'cart_courses': cart_courses})


@login_required
def add_to_cart(request, course_id):
    course = Course.objects.get(id=course_id)
    # Check if the course is already in the user's cart
    if course in request.user.student.cart.all():
        messages.info(request, "This course is already in your cart.")
    else:
        request.user.student.cart.add(course)
        messages.success(request, "Course added to cart successfully.")
    return redirect('view_course_details', course_id=course_id)


def remove_from_cart(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        if request.user.is_authenticated:  # Ensure the user is authenticated
            student = request.user.student
            if student.cart.filter(pk=course_id).exists():
                student.cart.remove(course)
                return redirect('view_cart')  # Redirect to the cart page after removal
    return redirect('view_cart')

def add_to_wishlist(request, course_id):
    if request.method == 'POST':
        course = Course.objects.get(id=course_id)
        student = request.user.student
        student.wishlist.add(course)  # Assuming 'wishlist' is the name of the ManyToManyField in the Student model
        return redirect('view_course_details', course_id=course_id)
    else:
        return redirect('course_catalog')  # Redirect to course catalog if not a POST request

def wishlist(request):
    student = request.user.student
    wishlist_courses = student.wishlist.all()
    return render(request, 'wishlist.html', {'wishlist_courses': wishlist_courses})


def remove_from_wishlist(request, course_id):
    student = request.user.student
    course = student.wishlist.get(id=course_id)
    student.wishlist.remove(course)
    return redirect('wishlist')


def support(request):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description')
        attachment = request.FILES.get('attachment')

        Ticket.objects.create(
            user=request.user,
            reason=reason,
            description=description,
            attachment=attachment
        )
        return redirect('support')

    tickets = Ticket.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'support.html', {'tickets': tickets})


@login_required
def update_profile(request):
    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('update_profile')  # Redirect to update profile page after successful update
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})


@login_required
def account_security(request):
    if request.method == 'POST':
        email_form = EmailChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if email_form.is_valid():
            email_form.save()
            return redirect('update_profile')
        elif password_form.is_valid():
            password_form.save()
            # Update the session to prevent users from being logged out after changing password
            update_session_auth_hash(request, request.user)
            # Redirect to update profile page after successful update
            return redirect('update_profile')
    else:
        email_form = EmailChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'account_security.html', {'email_form': email_form, 'password_form': password_form})


@login_required
def educational_details(request):
    return render(request, 'educational_details.html')


@login_required
def add_work_experience(request):
    work_experience_form = WorkExperienceForm()
    if request.method == 'POST':
        work_experience_form = WorkExperienceForm(request.POST)
        if work_experience_form.is_valid():
            work_experience = work_experience_form.save(commit=False)
            work_experience.user = request.user
            work_experience.save()
            messages.success(request, 'Work experience has been added successfully.')
            return redirect('educational_details')
    return render(request, 'add_work_experience.html', {'work_experience_form': work_experience_form})


@login_required
def add_education(request):
    education_form = EducationForm()
    if request.method == 'POST':
        education_form = EducationForm(request.POST)
        if education_form.is_valid():
            education = education_form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('educational_details')
    return render(request, 'add_education.html', {'education_form': education_form})


@login_required
def add_project(request):
    project_form = ProjectForm()
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('educational_details')
    return render(request, 'add_project.html', {'project_form': project_form})


@login_required
def privacy_settings(request):
    try:
        privacy_settings = request.user.privacysettings
    except PrivacySettings.DoesNotExist:
        privacy_settings = PrivacySettings(user=request.user)

    if request.method == 'POST':
        form = PrivacySettingsForm(request.POST, instance=privacy_settings)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
    else:
        form = PrivacySettingsForm(instance=privacy_settings)

    return render(request, 'privacy_settings.html', {'form': form})


@login_required
def notification_settings(request):
    try:
        settings = NotificationSettings.objects.get(user=request.user)
    except NotificationSettings.DoesNotExist:
        settings = NotificationSettings(user=request.user)

    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
    else:
        form = NotificationSettingsForm(instance=settings)

    return render(request, 'notification_settings.html', {'form': form})


@login_required
def referrals(request):
    if request.method == 'POST':
        referral_form = ReferralForm(request.POST)
        if referral_form.is_valid():
            referral = referral_form.save(commit=False)
            referral.user = request.user
            referral.save()
            return redirect('referrals')
    else:
        referral_form = ReferralForm()
    return render(request, 'referrals.html', {'referral_form': referral_form})


@login_required
def payment_history(request):
    payments = PaymentHistory.objects.filter(user=request.user)
    return render(request, 'payment_history.html', {'payments': payments})


@csrf_exempt
@login_required
def add_note(request, course_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        course = get_object_or_404(Course, id=course_id)
        student = get_object_or_404(Student, user=request.user)
        note = Note.objects.create(course=course, student=student, content=content)
        return JsonResponse({'status': 'success', 'note': {'content': note.content, 'created_at': note.created_at}})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_notes(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(Student, user=request.user)
    notes = Note.objects.filter(course=course, student=student).values('content', 'created_at')
    return JsonResponse({'status': 'success', 'notes': list(notes)})