from django.urls import include, path
from .views import UserDetail, PostDetail, InteractionDetail, registerUsers, CustomTokenObtainPairView, UpdatePostRating, EstimateRating, UsernameSearchView

urlpatterns = [
    #Misma para get  y post 
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', registerUsers.as_view(), name="register"),
    path('user/', UserDetail.as_view(), name="user"),
    path('user/<int:pk>', UserDetail.as_view(), name='user-detail'),
    path('post/', PostDetail.as_view(), name='post'),
    path('post/<int:pk>', PostDetail.as_view(), name='post-detail'),
    path('interaction/', InteractionDetail.as_view(), name='interaction'),
    path('interaction/<int:pk>/', InteractionDetail.as_view(), name='interaction-detail'),
    path('rating/', UpdatePostRating.as_view(), name='rating'),
    path('post/estimate/<int:pk>/', EstimateRating.as_view(), name='estimate-rating'),
    path('usernames/search/', UsernameSearchView.as_view(), name='username-search'),
]
