from django.db import models


# Create your models here.


class FileInfo(models.Model):
    class Meta:
        verbose_name = '文件'
        verbose_name_plural = verbose_name

    file_name = models.CharField('文件名', max_length=255)
    file = models.FileField('文件', upload_to="file/")

    def __str__(self):
        return self.file.name
