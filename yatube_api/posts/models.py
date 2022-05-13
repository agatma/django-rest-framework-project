from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             help_text='Группа, к которой относится пост',
                             verbose_name='Название группы',
                             )
    slug = models.SlugField(unique=True, )
    description = models.TextField(
        help_text='Описание группы',
        verbose_name='Описание группы',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(help_text='Введите текст поста',
                            verbose_name='Содержание поста')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text='Дата публикации поста (автоматически определяется)',
        verbose_name='Дата публикации поста',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        help_text='Автор поста',
        verbose_name='Автор поста',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        null=True,
        help_text='Загрузите картинку',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        help_text='Группа, к которой будет относиться пост',
        verbose_name='Название группы',
    )

    class Meta:
        verbose_name = 'Посты'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:settings.POST_SYMBOLS]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text[:settings.POST_SYMBOLS]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_user',
        verbose_name='подписчик',
        help_text='Пользователь, который подписывается.',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_user',
        verbose_name='автор',
        help_text='Пользователь, на которого подписываются.',
    )

    class Meta:
        ordering = ('-following',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow')
        ]

    def __str__(self):
        return (f'user - {self.user} '
                f'following - {self.following}')

