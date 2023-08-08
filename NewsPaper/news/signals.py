from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Post, User, Category, PostCategory
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_news(sender, instance, action, **kwargs):
        link = f"http://127.0.0.1:8000/news/{str(instance.id)}/"
        # print(link)
        if action == 'post_add' and instance.postCategory.all():
            userlist = []
            for category in instance.postCategory.all():
                for user in category.subscriber.all():
                    userlist.append(user.username)


            if userlist:
                userlistunique = list(set(userlist))

                for user in userlistunique:
                    usertoemail = User.objects.get(username = user)

                    html_content = render_to_string('news/news_send.html', {'post': instance, "user": user, "link": link, })

                    msg = EmailMultiAlternatives(
                        subject=f'Добавлена новость по теме:{instance.topic} от {instance.date}',
                        body=instance.contents ,
                        from_email='alexander.hafisov@yandex.ru',
                        to= [usertoemail.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()