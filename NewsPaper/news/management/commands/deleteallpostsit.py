from django.core.management.base import BaseCommand, CommandError
from news.models import Post


class Command(BaseCommand):
    help = ' Удаление всех постов в категории IT'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.write('Do you really want to delete all products? yes/no')
        answer = input()

        if answer == 'yes':
            for post_unit in Post.objects.all():
                for category_unit in post_unit.postCategory.all():
                    if category_unit.theme == "IT":
                        self.stdout.write('Пост id %s удален, тема: %s' % (post_unit.id, post_unit.topic))
                        # post_unit.delete() # Улаляем все посты с категорией IT

            self.stdout.write(self.style.SUCCESS('Successfully deleted all existing IT posts'))
            return

        self.stdout.write(self.style.ERROR('Action was cancelled'))