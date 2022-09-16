from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)
    subcategory = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.subcategory:
            return f"{self.title}-->{self.subcategory}"
        return f"{self.title}"