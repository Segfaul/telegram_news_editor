from django.db import models
from django.urls import reverse


class Post(models.Model):

    title = models.CharField(max_length=255, verbose_name="Title")

    description = models.TextField(blank=True, verbose_name="Description")

    cover = models.URLField(null=True, verbose_name="Cover", blank=True)

    publication_date = models.DateTimeField(verbose_name="Publication Date", null=True)
    modified_date = models.DateTimeField(auto_now=True, verbose_name="Modified Date")

    is_published = models.BooleanField(default=False, verbose_name="Is published?")

    origin_link = models.URLField(blank=True, verbose_name="Origin link", null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-publication_date', 'title']
