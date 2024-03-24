from rest_framework import routers

from core.auth.viewsets import RegisterViewSet, LoginViewSet, RefreshViewSet
from core.user.viewsets import UserViewSet, ReferralCodeViewSet, ReferralViewSet, ShareRefCodeViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'referral_code', ReferralCodeViewSet, basename='referral-code')
router.register(r'referrals', ReferralViewSet, basename='referral-detail')
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')
router.register(r'share', ShareRefCodeViewSet, basename='share-code')

urlpatterns = [*router.urls]

