from django.db import models


class Word(models.Model):
    trad = models.CharField(max_length=1000)
    pinyin = models.CharField(max_length=1000)
    sim = models.CharField(max_length=1000)
    eng = models.CharField(max_length=1000)
    ko = models.CharField(max_length=1000)
    ind = models.CharField(max_length=1000)
    es = models.CharField(max_length=1000)
    ur = models.CharField(max_length=1000)
    tl = models.CharField(max_length=1000)
    de = models.CharField(max_length=1000)
    hu = models.CharField(max_length=1000)
    vi = models.CharField(max_length=1000)

    def __str__(self):
        return f'[{self.id}] {self.trad}'
