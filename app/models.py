from django.db import models

# Create your models here.
class Country_Code(models.Model):
    name = models.CharField(max_length=1000)
    short_name = models.CharField(max_length=1000)
    dial_code = models.CharField(max_length=1000)
    flag = models.URLField(max_length=1000)
    class Meta:
        ordering = ['name',]

    def save(self, *args, **kwargs):
        self.full_clean() # calls self.clean() as well cleans other fields
        return super(Country_Code, self).save(*args, **kwargs)

    def __str__(self):
        return self.country