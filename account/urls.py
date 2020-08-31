from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import my_profile_view, invites_received_view, ProfileLIstView, invite_profiles_list_view, send_invitation, \
    remove_from_friends, accept_invitation, reject_invitation, invite_profiles_list_views, friends_list,\
    people_you_mayKnow, invites_received_view2, user_search

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites2/', invites_received_view2, name='my-invites-view2'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('all-profiles/', ProfileLIstView.as_view(), name='all-profiles-view'),
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
    path('to-invites/', invite_profiles_list_views, name='invite-profiles-views'),
    path('send-invite/', send_invitation, name='send-invite'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
    path('my-invites/accept', accept_invitation, name='accept-invite'),
    path('my-invites/reject', reject_invitation, name='reject-invite'),
   path('friends', friends_list, name='friends'),
    path('peopleyoumayknow', people_you_mayKnow, name='peopleyoumayknow'),
    path('search', user_search, name='search'),

]
