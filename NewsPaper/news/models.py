from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Sum

# Create your models here.
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser.username}'

    @property
    def above_zero_rating(self):
        return self.authorRating > 0

    def update_rating(self):
        # Count author's  sum rating of all his articles (instance Author)
        if self.post_set.filter(category="AR").exists():
            postRat = self.post_set.filter(category="AR").aggregate(postRatingSum=Sum("rating"))
            postRating = postRat.get('postRatingSum')
        else:
            postRating = 0

        # Count author's  sum rating of all his comments (instance Author)
        if self.authorUser.comment_set.all().exists():
            commentRat = self.authorUser.comment_set.all().aggregate(commentRatingSum=Sum("rating"))
            commentRating = commentRat.get('commentRatingSum')
        else:
            commentRating = 0

        # Count sum rating of all comments to author's articles (instance Author)
        if self.post_set.filter(category="AR", postAuthor=self).exists():
            commentRatAllUsers = self.post_set.filter(category="AR", postAuthor=self).\
                aggregate(commentRatingAllUsersSum=Sum("rating"))
            commentRatingAllUsers = commentRatAllUsers.get('commentRatingAllUsersSum')
        else:
            commentRatingAllUsers = 0

        self.authorRating = postRating * 3 + commentRating + commentRatingAllUsers
        self.save()

class Category(models.Model):
    theme = models.CharField(max_length=64, unique=True)
    subscriber = models.ManyToManyField(User, through="CategoryUser")

    def __str__(self):
        return f'{self.theme}'
class CategoryUser(models.Model):
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    userThrough = models.ForeignKey(User, on_delete=models.CASCADE)

class Post(models.Model):
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')

    ARTICLE = "AR"
    NEWS = "NE"
    post_type = (
        (ARTICLE, 'статья'),
        (NEWS, 'новость')
    )
    category = models.CharField(max_length=2, choices=post_type, default=NEWS, verbose_name='Категория')
    date = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through="PostCategory", verbose_name='Разделы')
    topic = models.CharField(max_length=64,  verbose_name='Тема')
    contents = models.TextField(verbose_name='Содержание')
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'на тему "{self.topic}"'

    def get_absolute_url(self):
        # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.contents[0:124] + "..."

class PostCategory(models.Model):
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'От пользователя {self.commentUser.username} на тему "{self.commentPost.topic}"'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


