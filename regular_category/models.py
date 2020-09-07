from django.db import models


class RegularCategory(models.Model):
    title = models.CharField("标题", max_length=255, null=True)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title
        }

    def search(self):
        return {
            "id": self.id,
            "title": self.title
        }

    class Meta:
        verbose_name = "习惯养成的类别"
        verbose_name_plural = verbose_name
