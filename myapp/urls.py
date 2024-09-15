from django.urls import include, path
from myapp import views
from .views import UserDetail, PostDetail, InteractionDetail

urlpatterns = [
    #Misma para get  y post 
    path('user/', UserDetail.as_view(), name="user"),
    path('user/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('post/', PostDetail.as_view(), name='post'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('interaction/', InteractionDetail.as_view(), name='interaction'),
    path('interaction/<int:pk>/', InteractionDetail.as_view(), name='interaction-detail')
]
