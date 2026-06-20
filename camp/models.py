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


class DonationManager(models.Manager):
    def donation_validator(self, data):
        errors = {}
        try:
            amount = float(data.get('amount', 0))
            if amount < 1:
                errors['amount'] = 'الحد الأدنى للتبرع دولار واحد'
        except (ValueError, TypeError):
            errors['amount'] = 'يرجى إدخال مبلغ صحيح'
        is_anonymous = data.get('is_anonymous') == 'on'
        if not is_anonymous:
            if not data.get('name', '').strip():
                errors['name'] = 'الاسم مطلوب'
            email = data.get('email', '').strip()
            if not email or '@' not in email:
                errors['email'] = 'يرجى إدخال بريد إلكتروني صحيح'
        return errors


class Donation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المبلغ')
    name = models.CharField(max_length=200, blank=True, verbose_name='الاسم')
    email = models.EmailField(blank=True, verbose_name='البريد الإلكتروني')
    message = models.TextField(blank=True, verbose_name='الرسالة')
    is_anonymous = models.BooleanField(default=False, verbose_name='مجهول الهوية')
    story = models.ForeignKey('Article', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='قصة مرتبطة')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاريخ التبرع')

    objects = DonationManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'تبرع'
        verbose_name_plural = 'التبرعات'

    def __str__(self):
        label = 'مجهول' if self.is_anonymous else self.name
        return f'{label} — ${self.amount}'


class ContactMessageManager(models.Manager):
    def contact_validator(self, data):
        errors = {}
        if not data.get('name', '').strip():
            errors['name'] = 'الاسم مطلوب'
        email = data.get('email', '').strip()
        if not email or '@' not in email:
            errors['email'] = 'يرجى إدخال بريد إلكتروني صحيح'
        if not data.get('phone', '').strip():
            errors['phone'] = 'رقم الهاتف مطلوب'
        if not data.get('subject', '').strip():
            errors['subject'] = 'يرجى اختيار موضوع الرسالة'
        if len(data.get('message', '').strip()) < 10:
            errors['message'] = 'الرسالة يجب أن تكون 10 أحرف على الأقل'
        return errors


class ContactMessage(models.Model):
    name = models.CharField(max_length=200, verbose_name='الاسم')
    email = models.EmailField(verbose_name='البريد الإلكتروني')
    phone = models.CharField(max_length=30, blank=True, verbose_name='الهاتف')
    subject = models.CharField(max_length=200, verbose_name='الموضوع')
    message = models.TextField(verbose_name='الرسالة')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاريخ الإرسال')

    objects = ContactMessageManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'رسالة تواصل'
        verbose_name_plural = 'رسائل التواصل'

    def __str__(self):
        return f'{self.name} — {self.subject}'


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
