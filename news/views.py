from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Category, User
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'flatpages/post.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(
            name='authors').exists()
        return context

class PostDetail(DetailView):
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'flatpages/postpk.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель gjcnjd
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'flatpages/post_edit.html'
    permission_required = ('news.add_post',)

class PostUpdate(PermissionRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'
    permission_required = ('news.change_post',)

class PostDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def authorized_page(request):
    return render(request, 'flatpages/authorized_page.html')

@login_required
def become_author_view(request):
    author_group = Group.objects.get(name='authors')
    author_group.user_set.add(request.user)
    return redirect('/')

class CategoryListView(ListView):
    model = Post
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'flatpages/subscribe.html', {"category": category, "message": message})

