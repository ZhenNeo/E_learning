from django.urls import path
from.views import *


urlpatterns = [
    path('',do_login,name='login'),
    path('student-signup/',student_signup,name='student-signup'),
    path('verify-otp',verify_otp,name='verify_otp'),
    path('logout/', logout_user, name='logout'),

    path('course_catalog', course_catalog, name='course_catalog'),
    path('career_roadmap', career_roadmap, name='career_roadmap'),

    path('mentorship_page/', homepage, name='mentorship_page'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
    path('course/<int:course_id>/', view_course_details, name='view_course_details'),
    path('enroll-course/<int:course_id>/', enroll_course, name='enroll_course'),
    path('course_payment/<int:course_id>/', course_payment, name='course_payment'),
    path('enrolled-courses/', enrolled_course, name='enrolled_course'),
    path('enrolled-courses/<int:course_id>/start-course', start_course, name='start_course'),
    path('start-course/<int:course_id>/previous_question_papers/', previous_question_papers,
         name='previous_question_papers'),

    path('community/',community_platform, name='community_platform'),
    path('community/add_post/',add_post, name='add_post'),
    path('community/add_comment/<int:post_id>/',add_comment, name='add_comment'),

    path('like_post/<int:post_id>/',like_post, name='like_post'),
    path('dislike_post/<int:post_id>/',dislike_post, name='dislike_post'),
    path('like_comment/<int:comment_id>/', like_comment, name='like_comment'),
    path('dislike_comment/<int:comment_id>/', dislike_comment, name='dislike_comment'),

    path('add-to-cart/<int:course_id>/', add_to_cart, name='add_to_cart'),
    path('view-cart/', view_cart, name='view_cart'),
    path('remove-from-cart/<int:course_id>/', remove_from_cart, name='remove_from_cart'),

    path('add_to_wishlist/<int:course_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('wishlist/remove/<int:course_id>/', remove_from_wishlist, name='remove_from_wishlist'),

    path('support/', support, name='support'),


    path('update_profile/', update_profile, name='update_profile'),
    path('account_security/', account_security, name='account_security'),
    path('educational_details/', educational_details, name='educational_details'),
    path('add_work_experience/', add_work_experience, name='add_work_experience'),
    path('add_education/', add_education, name='add_education'),
    path('add_project/', add_project, name='add_project'),
    path('privacy_settings/', privacy_settings, name='privacy_settings'),
    path('notification_settings/', notification_settings, name='notification_settings'),
    path('referrals/', referrals, name='referrals'),
    path('payment_history/', payment_history, name='payment_history'),


    path('courses/<int:course_id>/add_note/', add_note, name='add_note'),
    path('courses/<int:course_id>/get_notes/', get_notes, name='get_notes'),
]