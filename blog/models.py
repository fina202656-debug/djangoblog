
from django.db import models
from django.utils.text import slugify
from PIL import Image
from django.conf import settings
from pathlib import Path


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="posts",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="published",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
    )

    cover_image = models.ImageField(
        upload_to="post_covers/",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "post"
            new_slug = base_slug
            counter = 1

            while Post.objects.filter(
                slug=new_slug
            ).exclude(pk=self.pk).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = new_slug

        super().save(*args, **kwargs)

        if self.cover_image:
            try:
                image_path = self.cover_image.path

                with Image.open(image_path) as img:
                    img.thumbnail((800, 800))
                    img.save(image_path)

            except (OSError, ValueError):
                pass

    def __str__(self):
        return self.title
