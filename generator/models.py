from django.db import models


# Name class for holding ID, Name and Sex for that name
# WARNING: Name can appear 2 times because name could be bisex
class Name(models.Model):
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
    SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    )
    surname = models.CharField("Surname", max_length=60)
    sex = models.CharField(max_length=1, choices=SEX)

    def __str__(self):
        return self.name


# Category class for holding category_name as category and ID
class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


# Class Datatype for holding dataype and pointing to category
# Class connects category with datatype
class Datatype(models.Model):
    datatype = models.CharField(max_length=50)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.datatype


# Class Table
# It connects with Column (columnns)
class Table(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Class Column
# It connects datatype with column name and options
class Column(models.Model):
    column_name = models.CharField(max_length=200)
    datatype = models.ForeignKey(Datatype)
    # options = models.CharField(max_length=200, null=True, blank=True)
    table = models.ForeignKey(Table)

    def __str__(self):
        return self.column_name
