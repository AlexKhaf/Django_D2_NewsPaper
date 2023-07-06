from django_filters import FilterSet, CharFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from news.models import Post


# создаём фильтр
class PostFilter(FilterSet):
    # topic = CharFilter(label='Тема')
    # postAuthor__authorUser__username = CharFilter(label='Имя автора')
    # date = CharFilter(label='Дата')
    class Meta:
        model = Post

        # fields = ('postAuthor__authorUser__username', 'date')

        fields = {
                    # 'topic': ['icontains'],
                    'postAuthor__authorUser__username': ['icontains'],
                    'date': ['gt'],
                }