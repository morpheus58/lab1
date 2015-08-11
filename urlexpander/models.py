from django.db import models

# Create your models here.
class expandedurls(models.Model):
    destination_url = models.URLField()
    short_url = models.URLField()
    http_status_code = models.IntegerField()
    page_title = models.CharField(max_length=100)
