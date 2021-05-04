from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150, primary_key=True)
    price = models.IntegerField()


class OrderLog(models.Model):
    product = models.ForeignKey(Product, related_name='Product', on_delete=models.CASCADE, to_field='name',
                                db_column='name')
    created = models.DateTimeField()
    isCancel = models.BooleanField(default=False, null=False)


########################################################################################################################

# Proxy 모델
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class MyPerson(Person):
    class Meta:
        proxy = True

class OrderedPerson(Person):
    class Meta:
        proxy = True
        ordering = ['last_name']
