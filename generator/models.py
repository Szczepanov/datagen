from django.db import models


# Name class for holding ID, Name and Sex for that name
# WARNING: Name can appear 2 times because name could be bisex
class Name(models.Model):
    id = models.AutoField(primary_key=True)
    SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    )
    name = models.CharField("First name", max_length=50)
    sex = models.CharField(max_length=1, choices=SEX)

    def __str__(self):
        return self.name


# Surname class for holding ID, Surname and Sex for that surname
class Surname(models.Model):
    id = models.AutoField(primary_key=True)
    SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    )
    surname = models.CharField("Surname", max_length=60)
    sex = models.CharField(max_length=1, choices=SEX)

    def __str__(self):
        return self.name


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class DataType(models.Model):
    datatype = models.CharField(primary_key=True, max_length=50)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.datatype
#TODO
#add DataSetRow and modify DataSet to have name and key to DataSetRow
    
 # class DataSetRow(models.Model):
 #     id = models.AutoField(primary_key=True)
 #     column_name = models.CharField(max_length=200, default='ColumnName')
 #     data_type = models.ForeignKey('DataType', on_delete=models.SET_NULL, null=True)
 #     options = models.CharField(max_length=200, default='options')

class DataSet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='name1')
    column_name = models.CharField(max_length=200, default='ColumnName')
    data_type = models.ForeignKey('DataType', on_delete=models.SET_NULL, null=True)

    def generate(self):
        self.save()

    def __str__(self):
        return self.name

