from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, authorized_page, become_author_view,CategoryListView,subscribe
from django.views.decorators.cache import cache_page

urlpatterns = [

   path('', PostList.as_view(),name='post_list'),
   path('<int:pk>', cache_page(60) (PostDetail.as_view()), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('authorized_page/', authorized_page, name='authorized_page'),
   path('become_author/', become_author_view, name='become_author'),
   path('categories/<int:pk>', cache_page(60*5) (CategoryListView.as_view()), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe' )
]
