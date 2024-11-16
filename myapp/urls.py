from django.urls import include, path
from .views import UserDetail, PostDetail, InteractionDetail, RegisterUsers, UpdatePostRating, EstimateRating, UsernameSearchView, CustomTokenObtainPairView

urlpatterns = [
    # Same for GET and POST
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/refresh',RefreshTokenView.as_view(),name='refresh-token' ),
    path('register/', RegisterUsers.as_view(), name="register"),
    path('user/', UserDetail.as_view(), name="user"),
    path('user/<int:pk>', UserDetail.as_view(), name='user-detail'),
    path('post/', PostDetail.as_view(), name='post'),
    path('post/<int:pk>', PostDetail.as_view(), name='post-detail'),
    path('interaction/', InteractionDetail.as_view(), name='interaction'),
    path('interaction/<int:pk>/', InteractionDetail.as_view(), name='interaction-detail'),
    path('rating/', UpdatePostRating.as_view(), name='rating'),
    path('post/estimate/<int:pk>/', EstimateRating.as_view(), name='estimate_rating'),
    path('usernames/search/', UsernameSearchView.as_view(), name='username-search'),
    
]
