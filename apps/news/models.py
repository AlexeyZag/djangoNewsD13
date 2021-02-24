from django.db import models
from datetime import datetime, date
from django.core.cache import cache
from django.utils import timezone
# Create your models here.
from djangoNews2.settings import AUTH_USER_MODEL




class Author(models.Model):
    author = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        auth = self.author
        auth_id = Author.objects.get(author= auth).id
        sum_post = sum([i.rating_of_post for i in Post.objects.filter(author = auth_id)])

        sum_com = sum([i.com_rating for i in Comment.objects.filter(comment_user= auth)])

        sum_post_com = sum([comment.com_rating
                            for comment in Comment.objects.filter(comment_post__in = Post.objects.filter(author = auth_id))
                            if comment not in Comment.objects.filter(comment_user= auth)])

        self.rating = sum_post * 3 + sum_com + sum_post_com
        self.save()
        return self.rating

    def __str__(self):
        return f'{self.author}'

class Category(models.Model):
    tag = models.CharField(max_length= 100, unique=True)
    subscribers = models.ManyToManyField(AUTH_USER_MODEL, blank=True, null=True,
                                    related_name='subscription',
                                    verbose_name='Подписчики')

    def __str__(self):
        return f'{self.tag}'


class Post(models.Model):
    class Meta:
        verbose_name_plural  = "Новости"
    article = 'Статья'
    news = 'Новость'
    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name = "Автор")
    article_default_news = models.CharField(max_length = 7, choices = POSITIONS, default = news, verbose_name= 'Новость или статья')
    create_time = models.DateTimeField(auto_now_add = True, verbose_name= 'Дата создания')
    categories = models.ManyToManyField(Category, through= 'PostCategory', verbose_name= 'Тэг', related_name = 'categories')
    headline = models.CharField(max_length = 255, verbose_name= 'Заголовок')
    text = models.TextField()
    rating_of_post = models.IntegerField(default=0)
    likers = models.ManyToManyField(AUTH_USER_MODEL, blank=True, null=True,
                                    related_name='likers',
                                    verbose_name='Понравилось')
    dislikers = models.ManyToManyField(AUTH_USER_MODEL, blank=True, null=True,
                                    related_name='dislikers',
                                    verbose_name='Не понравилось')


    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с новостью
        return f'/news/{self.id}'


    def like(self):
        self.rating_of_post += 1
        self.save()

    def dislike(self):
        self.rating_of_post -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его



    def __str__(self):
        return f"Автор: {self.author}, вид работы: {self.article_default_news}, Заголовок: {self.headline}, оценка: {self.rating_of_post}, категории: {self.categories.all()}"


class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.category}'

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)
    com_text = models.TextField()
    com_time = models.DateTimeField(default=timezone.now)
    com_rating = models.IntegerField(default=0)

    def like(self):
        self.com_rating += 1
        self.save()
    def dislike(self):
        self.com_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_post}, {self.comment_user}, {self.com_rating}'

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с новостью
        return f'/news/{self.comment_post.id}'



#Category.objects.all().values('subscribers')
#Post.objects.get(pk=id).categories.all().values('tag')
#Category.objects.all()[2].subscribers.all().values('username')
#Category.objects.filter(tag='Спорт').values('subscribers__username').values()
#print(user in Category.objects.filter(tag='Спорт').values('subscribers__username')[0].values())
#Category.objects.get(tag= 'Спорт').subscribers.add(User.objects.get(username='author'))
#Category.objects.all()[0].id
#a = Post.objects.get(pk=4).categories.all().values('tag', 'id')
#a[0]['tag']
#Category.objects.filter(subscribers= User.objects.get(username='admin'))
#Category.objects.filter(subscribers= User.objects.get(username='admin')).values_list()
#Category.objects.filter(subscribers= User.objects.get(username=str(user))).filter(tag = 'Спорт').id
#Category.objects.all().get(pk=1)
#Category.objects.get(pk=1).subscribers.remove(User.objects.get(username='admin'))
#Author.objects.get(author= User.objects.get(username='admin'))
#Author.objects.all()
#Post.objects.get(pk=4).categories.all()
#Category.objects.get(tag=tag).subscribers.all()
#PostCategory.objects.all()
#Post.objects.filter(categories__tag= 'Спорт')
#Post.objects.filter(create_time__gt= datetime.fromtimestamp(datetime.timestamp(datetime.now()) - 604800), categories=tag).values('id')
#Comment.objects.filter(comment_post_id= 3)
#Comment.objects.get(pk = 3).comment_post.id
#Post.objects.get(pk = 3).author.update_rating()
#Author.objects.get(pk = 1).rating
#Category.objects.get(tag= 'политика'.title())
#Post.objects.filter(headline__icontains=)
#Post.objects.filter(author__in = 1).values()


