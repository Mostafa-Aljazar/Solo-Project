from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    BLOG = 'blog'
    STORY = 'story'
    TYPE_CHOICES = [(BLOG, 'مقال'), (STORY, 'قصة نجاح')]

    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='النوع')
    title = models.CharField(max_length=300, verbose_name='العنوان')
    brief = models.TextField(blank=True, verbose_name='مقدمة قصيرة')
    content = RichTextUploadingField(verbose_name='المحتوى', blank=True)
    cover_image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name='صورة الغلاف')
    reading_minutes = models.PositiveSmallIntegerField(default=3, verbose_name='وقت القراءة (دقائق)')
    is_published = models.BooleanField(default=True, verbose_name='منشور')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاريخ النشر')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'مقال / قصة'
        verbose_name_plural = 'المقالات والقصص'

    def __str__(self):
        return self.title

    def get_cover_image(self):
        if self.cover_image:
            return self.cover_image.url
        return None


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
