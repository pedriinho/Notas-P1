from django.db import models

# Create your models here.
class Classroom(models.Model):
    name = models.CharField(max_length=10, unique=True)
    id_list1 = models.CharField(max_length=10)
    id_list2 = models.CharField(max_length=10)
    id_list3 = models.CharField(max_length=10)
    id_list4 = models.CharField(max_length=10)
    id_list5 = models.CharField(max_length=10)
    id_list6 = models.CharField(max_length=10)
    id_list7 = models.CharField(max_length=10)
    id_list8 = models.CharField(max_length=10)
    id_test1 = models.CharField(max_length=10)
    id_test2 = models.CharField(max_length=10)
    id_test3 = models.CharField(max_length=10)
    id_test4 = models.CharField(max_length=10)
    id_reav = models.CharField(max_length=10)
    id_final = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    course = models.CharField(max_length=3)
    id_huxley = models.IntegerField(default=0)
    list1 = models.FloatField(default=0.0)
    list2 = models.FloatField(default=0.0)
    list3 = models.FloatField(default=0.0)
    list4 = models.FloatField(default=0.0)
    list5 = models.FloatField(default=0.0)
    list6 = models.FloatField(default=0.0)
    list7 = models.FloatField(default=0.0)
    list8 = models.FloatField(default=0.0)
    test1 = models.FloatField(default=0.0)
    test2 = models.FloatField(default=0.0)
    test3 = models.FloatField(default=0.0)
    test4 = models.FloatField(default=0.0)
    reav = models.FloatField(default=0.0)
    final = models.FloatField(default=0.0)
    mean = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)
    situation = models.CharField(max_length=20, default='EM ANÁLISE')

    def __str__(self):
        return self.name