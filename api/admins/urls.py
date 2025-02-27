from django.urls import path
from admins.views import *
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

urlpatterns = [
    path('admins/', UserRegistrationView.as_view()),
    path('login/', CustomUserLoginView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('logout/', TokenBlacklistView.as_view()),
    path('user-list/', UserListView.as_view()),
    path('user-profile/', UserProfileView.as_view()),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('admins-approve/<int:user_id>/', AdminApprovalView.as_view(), name='admins-approve'),
    path('admins-users/', AdminUserListView.as_view(), name='admins-user-list'),
    path('admins-reject/<int:user_id>/', AdminRejectUserView.as_view(), name='admins-reject'),
]