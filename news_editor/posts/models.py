from django.db import models
from django.urls import reverse


class Post(models.Model):

    title = models.CharField(max_length=255, verbose_name="Заголовок")

    description = models.TextField(blank=True, verbose_name="Описание")

    cover = models.ImageField(null=True, upload_to="photos/%Y/%m/%d/", verbose_name="Обложка", blank=True)

    publication_date = models.DateTimeField(verbose_name="Дата публикации", null=True)
    modified_date = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    is_published = models.BooleanField(default=False, verbose_name="Опубликован ли?")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-publication_date', 'title']
