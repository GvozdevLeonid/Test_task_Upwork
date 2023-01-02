from django.db import models


class URL(models.Model):
    url = models.URLField()
