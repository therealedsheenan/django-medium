from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    text = models.TextField()
    created_date = timezone.now()
    published_date = models.DateTimeField(blank=True, null=True)
    updated_date = timezone.now()

    def publish_update(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comments=True)

    # redirect when instance is saved
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=250)
    text = models.TextField()
    created_date = timezone.now()
    approved_comment = models.BooleanField(default=False)

    def approve_comment(self):
        self.approved_comment = True
        self.save()

    # redirect when instance is saved
    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
