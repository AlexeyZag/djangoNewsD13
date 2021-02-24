from django.core.management.base import CommandError, BaseCommand
from apps.news.models import Post, Category

class Command(BaseCommand):
    help = 'Delete all news'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('tag', nargs='+', type=str)
    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        print(options['tag'][0].title())
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all products? yes/no')  # спрашиваем пользователя действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            Post.objects.filter(categories= Category.objects.get(tag= options['tag'][0].title())).delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted news!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим что в доступе отказано