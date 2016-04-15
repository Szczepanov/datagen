from django.db import models


# Create your models here.


class DataSet(models.Model):
    name = models.TextField(default='name1')
    country = models.TextField(default='All')
    column_name = models.TextField(default='name')
    data_type = models.TextField(default='names')
    rows_number = models.IntegerField(default=1)

    def generate(self):
        self.save()

    def __str__(self):
        return self.name
