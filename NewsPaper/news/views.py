from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from django.contrib.auth import logout
from .models import Post, Category, Author, User
from search.filters import PostFilter # импортируем недавно написанный фильтр
from .forms import NewsForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
       premium_group.user_set.add(user)

    authorlist = []
    for author in Author.objects.all():
        authorlist.append(author.authorUser)
    if request.user not in authorlist:
        Author.objects.create(authorUser = request.user)

    return redirect('/news/')

@login_required
def downgrade_me(request):
   user = request.user
   premium_group = Group.objects.get(name='authors')
   if request.user.groups.filter(name='authors').exists():
      premium_group.user_set.remove(user)

   # authorlist = []
   # for author in Author.objects.all():
   #     authorlist.append(author.authorUser)
   # if request.user in authorlist:
   #     Author.objects.get(authorUser=request.user).delete()

   return redirect('/news/')

def subscribe(request, pk):
    category = Category.objects.get(pk = pk)
    category.subscriber.add(request.user.id)

    return HttpResponseRedirect(reverse('category', args = [pk]))

def unsubscribe(request, pk):
    category = Category.objects.get(pk = pk)
    category.subscriber.remove(request.user.id)

    return HttpResponseRedirect(reverse('category', args=[pk]))

# то же самое, только в отношении одного объекта
# ipad = Product.objects.get(name="iPad")
# apple.product_set.remove(ipad)

def weekly_emailing():
    day = datetime.now() - timedelta(days=7)
    week_posts = Post.objects.filter(date__gt = day)

    all_users = User.objects.all()

    postlist_id = []
    for user in all_users:
        for post_unit in week_posts:
            for cat in post_unit.postCategory.all():
                if user in cat.subscriber.all():
                    postlist_id.append(post_unit.id)

        if postlist_id:
            postlist_unique_id = list(set(postlist_id))
            print(postlist_unique_id, user.username)

            html_content = render_to_string('news/news_emailing.html', {'posts':week_posts , "user": user,
                                                                        "postlist_unique_id": postlist_unique_id, })

            msg = EmailMultiAlternatives(
                    subject=f'Список новостей за неделю',
                    body="",
                    from_email='alexander.hafisov@yandex.ru',
                    to=[user.email],
                )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            postlist_id = []
            print("Письмо отправлено", user.email)

class NewsList(LoginRequiredMixin, ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by("-date" )
    paginate_by = 7

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        # context['categories'] = Category.objects.all()
        # context['form'] = ProductForm()

        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

# создаём представление, в котором будут детали конкретного отдельного товара
class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id = self.kwargs['pk'])
        context['subscribers'] = category.subscriber.all()
        return context

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

    def post(self, request, *args, **kwargs):
        # super().post(request, *args, **kwargs)

        post = Post(
            category = request.POST['category'],
            topic = request.POST['topic'],
            postAuthor_id = request.POST['postAuthor'],
            contents=request.POST['contents'],
        )

        d = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        author = Author.objects.get(authorUser=post.postAuthor.authorUser)
        posts_all = Post.objects.filter(postAuthor=author, date__gt=d)
        posts_all_count = posts_all.count()

        if posts_all_count < 3:
            post.save()
            posts_all_count += 1

            catlist = request.POST.getlist('postCategory')
            if catlist:
                post.postCategory.set(catlist,)
                post.save()
        else:
            return render(request, template_name='news/postcancelled.html', context={'author': author,})
    #
    #     userlist = []
    #     for category in post.postCategory.all():
    #         for user in category.subscriber.all():
    #             userlist.append(user.username)
    #
    #     if userlist:
    #         userlistunique = list(set(userlist))
    #
    #         for user in userlistunique:
    #             usertoemail = User.objects.get(username = user)
    #             # получем html
    #             html_content = render_to_string('news/news_send.html', {'post': post, "user": user, })
    #
    #             msg = EmailMultiAlternatives(
    #                 subject=f'{post.topic}',
    #                 body=post.contents ,
    #                 from_email='alexander.hafisov@yandex.ru',
    #                 to= [usertoemail.email],
    #             )
    #             msg.attach_alternative(html_content, "text/html")  # добавляем html
                # msg.send()  # отсылаем

        return render(request, template_name='news/postallowed.html', context={'author': author, 'posts_all_count': posts_all_count })

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