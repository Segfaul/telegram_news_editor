from django.urls import path
from .views import *

urlpatterns = [
    path('', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('post', PostListView.as_view(), name='post_list'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/update/delete-cover/', PostDeleteCoverView.as_view(), name='post_delete_cover'),

    path('post/<int:pk>/publish/', PostPublishView.as_view(), name='post_publish'),
    path('post/<int:pk>/un_publish/', PostUnPublishView.as_view(), name='post_un_publish'),
]
