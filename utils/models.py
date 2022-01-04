from django.db import models


class Word(models.Model):
    trad = models.CharField(max_length=100)
    pinyin = models.CharField(max_length=100)
    sim = models.CharField(max_length=100)
    eng = models.CharField(max_length=100)
    ko = models.CharField(max_length=100)
    ind = models.CharField(max_length=100)
    es = models.CharField(max_length=100)
    ur = models.CharField(max_length=100)
    tl = models.CharField(max_length=100)
    de = models.CharField(max_length=100)
    hu = models.CharField(max_length=100)
    vi = models.CharField(max_length=100)

    def __str__(self):
        return f'[{self.id}] {self.trad}'
