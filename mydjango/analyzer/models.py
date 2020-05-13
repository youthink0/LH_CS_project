from django.db import models

class CrawlPage(models.Model):
    title = models.CharField(max_length = 100)
    category = models.CharField(max_length = 100)
    segment = models.CharField(max_length = 100)
    host = models.CharField(max_length = 100)
    url = models.CharField(max_length = 100)

    class Meta:
        db_table = "CrawlPage"

    def __str__(self):
        return self.title


