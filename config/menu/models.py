from django.db import models

from django.urls import reverse


class Menu(models.Model):
    title = models.CharField(max_length=20, verbose_name="Название меню")
    slug = models.SlugField(
        max_length=255,
        verbose_name="Слаг",
        null=True,
    )
    named_url = models.CharField(
        max_length=255,
        verbose_name="Named URL",
        blank=True,
    )

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.title

    def get_full_path(self):
        if self.named_url:
            url = reverse(self.named_url)
        else:
            url = "/{}/".format(self.slug)
        return url


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        verbose_name="Элемент меню",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        verbose_name="Верхний уровень меню",
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=100, verbose_name="Название элемента"
    )
    url = models.CharField(
        max_length=255, verbose_name="Ссылка", blank=True
    )
    named_url = models.CharField(
        max_length=255, verbose_name="Named URL", blank=True,
    )

    class Meta:
        verbose_name = "Элемент меню"
        verbose_name_plural = "Элементы меню"

    def get_url(self):
        if self.named_url:
            url = reverse(self.named_url)
        elif self.url:
            url = self.url
        else:
            url = "/"

        return url

    def __str__(self):
        return self.title
