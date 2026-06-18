from django.db import models


class HeroSlide(models.Model):
    title = models.CharField(max_length=200, verbose_name='العنوان')
    description = models.TextField(verbose_name='الوصف')
    tag = models.CharField(max_length=100, blank=True, verbose_name='الوسم')
    image = models.ImageField(upload_to='hero/', verbose_name='الصورة')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='الترتيب')
    is_active = models.BooleanField(default=True, verbose_name='نشط')

    class Meta:
        ordering = ['order']
        verbose_name = 'الشريحة الرئيسية'
        verbose_name_plural = 'الشرائح الرئيسية'

    def __str__(self):
        return self.title


class SiteStatistic(models.Model):
    label = models.CharField(max_length=100, verbose_name='التسمية')
    value = models.PositiveIntegerField(verbose_name='القيمة')
    description = models.CharField(max_length=200, verbose_name='الوصف')
    icon_name = models.CharField(max_length=50, verbose_name='اسم الأيقونة')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='الترتيب')

    class Meta:
        ordering = ['order']
        verbose_name = 'إحصائية الموقع'
        verbose_name_plural = 'إحصائيات الموقع'

    def __str__(self):
        return f'{self.label}: {self.value}'


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name='العنوان')
    description = models.TextField(verbose_name='الوصف')
    icon_name = models.CharField(max_length=50, verbose_name='اسم الأيقونة')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='الترتيب')
    is_active = models.BooleanField(default=True, verbose_name='نشط')

    class Meta:
        ordering = ['order']
        verbose_name = 'خدمة'
        verbose_name_plural = 'الخدمات'

    def __str__(self):
        return self.title
