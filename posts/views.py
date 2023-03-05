from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter, SearchFilter
from .forms import PostFormArtcl, PostFormNews


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
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


class CategoryPostsList(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = "category_items_list"

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        qs = Post.objects.filter(category_id=self.category).order_by('-created_at')
        print(qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    print(user)
    cat = Category.objects.get(id=pk)
    print(cat)
    cat.subscribers.add(user)
    msg = "You've been subscribed to"
    return render(request, 'subscribe.html', {'category': cat, 'message': msg})


class SearchList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'searchposts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = SearchFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtersearch'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreateArtcl(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('posts.add_post',)
    raise_exception = True
    form_class = PostFormArtcl
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = "ARTCL"
        return super().form_valid(form)


class PostCreateNews(PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_post',)
    form_class = PostFormNews
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = "NEWS"
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('posts.change_post',)
    form_class = PostFormArtcl
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('posts.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
