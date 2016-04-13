from django.db import models


# Create your models here.


class DataSet(models.Model):
    name = models.TextField()
    country = models.TextField()
    columnName = models.TextField()
    dataType = models.TextField()
    rowsNumber = models.TextField()

    def __init__(self):
        self.name = ''
        self.country = 'All'
        self.columnName = ''
        self.rowsNumber = '1'

    def generate(self):
        self.save()

    def __str__(self):
        return self.name
