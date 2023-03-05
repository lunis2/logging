from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def update_rating(self):
        post_r = self.post_set.aggregate(post_rating=Sum('rating'))
        cr = post_r.get('post_rating') * 3
        comments_r = self.user_id.comment_set.aggregate(comment_rating=Sum('rating'))
        self.rating = cr + comments_r.get('comment_rating')
        self.save()

    def __str__(self):
        return f'{self.user_id}'


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User)
    related_name = 'categories'

    def __str__(self):
        return f'{self.name}'

    def get_subscribers(self):
        return ",\n".join([str(p) for p in self.subscribers.all()])


class Post(models.Model):
    NEWS = "NEWS"
    ARTICLE = "ARTCL"
    CATEGORIES = ((NEWS, "News articles"), (ARTICLE, "Articles"))

    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=5, choices=CATEGORIES, default=NEWS)
    created_at = models.DateTimeField(auto_now_add=True)
    category_id = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def preview(self):
        txt = f"{self.text[:123]}..."
        return txt

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    to_category = models.ForeignKey(Category, on_delete=models.CASCADE)




class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
