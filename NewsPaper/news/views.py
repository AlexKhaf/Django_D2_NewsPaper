from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from django.contrib.auth import logout
from .models import Post
from search.filters import PostFilter # импортируем недавно написанный фильтр
from .forms import NewsForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def upgrade_me(request):
   user = request.user
   premium_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
      premium_group.user_set.add(user)
   return redirect('/news/')

@login_required
def downgrade_me(request):
   user = request.user
   premium_group = Group.objects.get(name='authors')
   if request.user.groups.filter(name='authors').exists():
      premium_group.user_set.remove(user)
   return redirect('/news/')

class NewsList(LoginRequiredMixin, ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by("category", "-date" )
    paginate_by = 2

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        # context['categories'] = Category.objects.all()
        # context['form'] = ProductForm()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

# создаём представление, в котором будут детали конкретного отдельного товара
class NewsDetail(LoginRequiredMixin, DetailView):
    # model = Post # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'news/news_detail.html' # название шаблона будет product.html
    context_object_name = 'one_news' # название объекта
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

# дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните. Остальное он сделает за вас
class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'news/news_create.html'
    form_class = NewsForm
    permission_required = ('news.add_post',)


# # дженерик для редактирования объекта
class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/news_create.html'
    form_class = NewsForm
    permission_required = ('news.change_post',)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class NewsDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'news/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class LogoutView(LoginRequiredMixin, TemplateView):
   template_name = 'news/logout.html'

   def get(self, request, *args, **kwargs):
      logout(request)
      return super().get(request, *args, **kwargs)

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['is_not_authors'] = True
       return context