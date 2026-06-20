from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.paginator import Paginator
from .models import Article, Donation, ContactMessage, HeroSlide, SiteStatistic, Service

SERVICE_ICONS = {
    'tent':     '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6"><path d="M3.5 21L14 3"/><path d="M20.5 21L10 3"/><path d="M15.5 21L12 15l-3.5 6"/><path d="M2 21h20"/></svg>',
    'apple':    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6"><path d="M12 6.528V3a1 1 0 0 1 1-1"/><path d="M18.237 21A15 15 0 0 0 22 11a6 6 0 0 0-10-4.472A6 6 0 0 0 2 11a15.1 15.1 0 0 0 3.763 10 3 3 0 0 0 3.648.648 5.5 5.5 0 0 1 5.178 0A3 3 0 0 0 18.237 21"/></svg>',
    'hospital': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6"><path d="M12 7v4"/><path d="M14 21v-3a2 2 0 0 0-4 0v3"/><path d="M14 9h-4"/><path d="M18 11h2a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h2"/><path d="M18 21V5a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16"/></svg>',
    'heart':    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6"><path d="m14.479 19.374-.971.939a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5a5.5 5.5 0 0 1 9.591-3.676.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5a5.2 5.2 0 0 1-.219 1.49"/><path d="M15 15h6"/><path d="M18 12v6"/></svg>',
    'book':     '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6"><path d="M12 7v14"/><path d="M16 12h2"/><path d="M16 8h2"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/><path d="M6 12h2"/><path d="M6 8h2"/></svg>',
    'wifi':     '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1" fill="currentColor" stroke="none"/></svg>',
    'shield':   '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="M9 12h6"/><path d="M12 9v6"/></svg>',
    'default':  '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="10"/></svg>',
}

MISSION_VALUES = [
    {'number': '01', 'title': 'الشفافية', 'desc': 'نلتزم بالوضوح التام في كل ما نقدمه، وندير مواردنا بمسؤولية تامة أمام المتبرعين والمستفيدين.'},
    {'number': '02', 'title': 'الإنسانية', 'desc': 'الإنسان هو بوصلتنا في كل قرار، نضع كرامة النازحين فوق كل اعتبار ونعمل بقلب واحد.'},
    {'number': '03', 'title': 'الاستدامة', 'desc': 'نبني برامج تُمكّن المجتمعات من الاعتماد على ذاتها، لا مجرد حلول مؤقتة تنتهي بانتهاء الأزمة.'},
]

ISLAMIC_QUOTE = {
    'type': 'آية كريمة',
    'arabic': 'مَّثَلُ الَّذِينَ يُنفِقُونَ أَمْوَالَهُمْ فِي سَبِيلِ اللَّهِ كَمَثَلِ حَبَّةٍ أَنبَتَتْ سَبْعَ سَنَابِلَ فِي كُلِّ سُنبُلَةٍ مِّائَةُ حَبَّةٍ ۗ وَاللَّهُ يُضَاعِفُ لِمَن يَشَاءُ ۗ وَاللَّهُ وَاسِعٌ عَلِيمٌ',
    'source': 'سورة البقرة — الآية ٢٦١',
}


def blog_list(request):
    qs = Article.objects.filter(content_type=Article.BLOG, is_published=True)
    total_count = qs.count()
    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'camp/written_content_list.html', {
        'page_obj': page_obj,
        'total_count': total_count,
        'page_title': 'المدونة',
        'hero_tag': 'المحتوى',
        'hero_desc': 'مقالات وأخبار ميدانية من قلب العمل الإنساني',
        'count_label': f'{total_count} مقال',
        'detail_url_name': 'blog_detail',
        'empty_title': 'لا توجد مقالات بعد',
        'empty_sub': 'ترقّب — سيتم نشر مقالات قريباً',
    })


def blog_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, content_type=Article.BLOG, is_published=True)
    return render(request, 'camp/written_content_detail.html', {
        'article': article,
        'list_url': '/blog/',
        'list_label': 'المدونة',
        'badge_label': 'مقال',
        'back_label': 'العودة إلى المدونة',
        'is_story': False,
    })


def story_list(request):
    qs = Article.objects.filter(content_type=Article.STORY, is_published=True)
    total_count = qs.count()
    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'camp/written_content_list.html', {
        'page_obj': page_obj,
        'total_count': total_count,
        'page_title': 'قصص النجاح',
        'hero_tag': 'إلهام وأمل',
        'hero_desc': 'قصص حقيقية لأشخاص حقيقيين استعادوا حياتهم بفضل دعمكم',
        'count_label': f'{total_count} قصة',
        'detail_url_name': 'story_detail',
        'empty_title': 'لا توجد قصص بعد',
        'empty_sub': 'ترقّب — سيتم نشر قصص ملهمة قريباً',
    })


def story_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, content_type=Article.STORY, is_published=True)
    return render(request, 'camp/written_content_detail.html', {
        'article': article,
        'list_url': '/success-stories/',
        'list_label': 'قصص النجاح',
        'badge_label': 'قصة نجاح',
        'back_label': 'العودة إلى قصص النجاح',
        'is_story': True,
    })


CONTACT_INFO = [
    {
        'title': 'الموقع',
        'value': 'قطاع غزة، فلسطين',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>',
    },
    {
        'title': 'البريد الإلكتروني',
        'value': 'info@alaqsacamp.org',
        'sub': 'نرد خلال 24 ساعة',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    },
    {
        'title': 'الهاتف',
        'value': '+970 000 000 000',
        'sub': 'الأحد — الخميس  8ص - 4م',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 8.82 2 2 0 015 6.64h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L9.91 13a16 16 0 006.08 6.08l.36-.36a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 20.92z"/></svg>',
    },
    {
        'title': 'ساعات العمل',
        'value': '8:00 ص — 4:00 م',
        'sub': 'الأحد إلى الخميس',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    },
]

SUBJECT_CHOICES = [
    ('استفسار عام', 'استفسار عام'),
    ('طلب تبرع', 'طلب تبرع'),
    ('التطوع والمشاركة', 'التطوع والمشاركة'),
    ('الإبلاغ عن مشكلة', 'الإبلاغ عن مشكلة'),
    ('طلب شراكة', 'طلب شراكة'),
    ('أخرى', 'أخرى'),
]

CONTACT_FAQS = [
    {'q': 'كيف يمكنني التبرع للمخيم؟', 'a': 'يمكنك التبرع بسهولة عبر صفحة التبرع على موقعنا، واختيار المبلغ المناسب لك. جميع التبرعات تُستخدم مباشرةً لدعم النازحين.'},
    {'q': 'هل يمكنني التطوع مع مخيم الأقصى؟', 'a': 'نعم، نرحب بكل متطوع! يمكنك التواصل معنا عبر نموذج التواصل وسنعود إليك بأقرب وقت ممكن.'},
    {'q': 'كيف أعرف أن تبرعي وصل للمستفيدين؟', 'a': 'نرسل لك تأكيداً فورياً بالبريد الإلكتروني، كما ننشر تقارير دورية شفافة عن استخدام الأموال.'},
    {'q': 'هل يمكنني زيارة المخيم بنفسي؟', 'a': 'نقدر اهتمامك الشخصي. يمكنك التواصل معنا لمعرفة إمكانية الزيارة بحسب الأوضاع الأمنية.'},
    {'q': 'ما هي الخدمات التي يقدمها المخيم؟', 'a': 'نقدم خدمات الإيواء، الغذاء والمياه، الرعاية الصحية، الدعم النفسي، التعليم، وخدمات الطوارئ.'},
    {'q': 'هل تقبلون التبرعات العينية؟', 'a': 'نقبل بعض التبرعات العينية. تواصل معنا أولاً لمعرفة ما نحتاجه تحديداً وكيفية إيصاله.'},
    {'q': 'ما مدى أمان بياناتي الشخصية؟', 'a': 'نلتزم بحماية بياناتك الشخصية بشكل كامل ولن نشاركها مع أي طرف ثالث.'},
    {'q': 'كم مدة الاستجابة لرسائل التواصل؟', 'a': 'نلتزم بالرد خلال 24 ساعة في أيام العمل (الأحد - الخميس).'},
]


def contact(request):
    errors = {}
    form_data = {}
    if request.method == 'POST':
        form_data = request.POST
        errors = ContactMessage.objects.contact_validator(request.POST)
        if not errors:
            name    = request.POST.get('name', '').strip()
            email   = request.POST.get('email', '').strip()
            phone   = request.POST.get('phone', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()

            ContactMessage.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, message=message,
            )

            from datetime import date
            plain_text = (
                f'الاسم: {name}\n'
                f'البريد: {email}\n'
                f'الهاتف: {phone}\n'
                f'الموضوع: {subject}\n\n'
                f'الرسالة:\n{message}'
            )
            from datetime import datetime
            received_at = datetime.now().strftime('%Y-%m-%d  %H:%M')
            html_content = f"""
<!DOCTYPE html>
<html lang="ar">
<head><meta charset="UTF-8"/></head>
<body style="margin:0;padding:40px 16px;background:#eef0ee;font-family:Arial,sans-serif;direction:rtl;color:#1a1a1a;">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:4px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.08);">

  <!-- Letterhead -->
  <tr>
    <td style="background:#345e40;padding:22px 32px;border-bottom:4px solid #2a4d33;">
      <table width="100%" cellpadding="0" cellspacing="0"><tr>
        <td style="color:#ffffff;">
          <p style="margin:0;font-size:19px;font-weight:700;letter-spacing:0.3px;">مخيم الأقصى</p>
          <p style="margin:3px 0 0;font-size:11px;color:rgba(255,255,255,0.6);">Al-Aqsa Camp — Humanitarian Relief Organization</p>
        </td>
        <td style="text-align:left;color:rgba(255,255,255,0.6);font-size:11px;white-space:nowrap;vertical-align:middle;">
          <p style="margin:0;">info@alaqsacamp.org</p>
          <p style="margin:3px 0 0;">Gaza, Palestine</p>
        </td>
      </tr></table>
    </td>
  </tr>

  <!-- Document title -->
  <tr>
    <td style="padding:24px 32px 16px;">
      <p style="margin:0 0 4px;font-size:11px;color:#999999;letter-spacing:1px;">إشعار رسمي — نموذج التواصل</p>
      <h2 style="margin:0;font-size:17px;color:#1a1a1a;font-weight:700;">طلب تواصل جديد: {subject}</h2>
    </td>
  </tr>

  <!-- Metadata bar -->
  <tr>
    <td style="padding:10px 32px;background:#f5f7f5;border-top:1px solid #e8ece8;border-bottom:1px solid #e8ece8;">
      <table width="100%" cellpadding="0" cellspacing="0"><tr>
        <td style="font-size:12px;color:#666666;"><strong>تاريخ الاستلام:</strong> {received_at}</td>
        <td style="font-size:12px;color:#666666;text-align:left;"><strong>المصدر:</strong> {request.build_absolute_uri('/contact-us/')}</td>
      </tr></table>
    </td>
  </tr>

  <!-- Sender details -->
  <tr>
    <td style="padding:24px 32px 0;">
      <p style="margin:0 0 12px;font-size:11px;font-weight:700;color:#345e40;text-transform:uppercase;letter-spacing:1px;padding-bottom:6px;border-bottom:2px solid #345e40;display:inline-block;">بيانات المُرسِل</p>
      <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e0e6e0;border-collapse:collapse;border-radius:4px;">
        <tr>
          <td style="padding:11px 16px;font-size:12px;color:#666666;font-weight:700;border-bottom:1px solid #e8ece8;background:#f5f7f5;width:130px;">الاسم الكامل</td>
          <td style="padding:11px 16px;font-size:13px;color:#1a1a1a;border-bottom:1px solid #e8ece8;">{name}</td>
        </tr>
        <tr>
          <td style="padding:11px 16px;font-size:12px;color:#666666;font-weight:700;border-bottom:1px solid #e8ece8;background:#f5f7f5;">البريد الإلكتروني</td>
          <td style="padding:11px 16px;font-size:13px;border-bottom:1px solid #e8ece8;"><a href="mailto:{email}" style="color:#345e40;text-decoration:none;font-weight:600;">{email}</a></td>
        </tr>
        <tr>
          <td style="padding:11px 16px;font-size:12px;color:#666666;font-weight:700;border-bottom:1px solid #e8ece8;background:#f5f7f5;">رقم الهاتف</td>
          <td style="padding:11px 16px;font-size:13px;color:#1a1a1a;border-bottom:1px solid #e8ece8;">{phone or '—'}</td>
        </tr>
        <tr>
          <td style="padding:11px 16px;font-size:12px;color:#666666;font-weight:700;background:#f5f7f5;">موضوع الرسالة</td>
          <td style="padding:11px 16px;font-size:13px;color:#1a1a1a;">{subject}</td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- Message body -->
  <tr>
    <td style="padding:24px 32px 0;">
      <p style="margin:0 0 12px;font-size:11px;font-weight:700;color:#345e40;text-transform:uppercase;letter-spacing:1px;padding-bottom:6px;border-bottom:2px solid #345e40;display:inline-block;">نص الرسالة</p>
      <div style="border:1px solid #e0e6e0;border-right:3px solid #345e40;padding:18px 20px;background:#f9fbf9;font-size:14px;line-height:2;color:#2e2e2e;border-radius:0 4px 4px 0;">
        {message}
      </div>
    </td>
  </tr>

  <!-- Action -->
  <tr>
    <td style="padding:24px 32px 28px;">
      <p style="margin:0 0 12px;font-size:12px;color:#777777;">للرد المباشر على هذه الرسالة:</p>
      <a href="mailto:{email}?subject=رد رسمي: {subject}"
         style="display:inline-block;background:#345e40;color:#ffffff;text-decoration:none;
                font-size:13px;font-weight:700;padding:11px 28px;border-radius:4px;">
        الرد على المُرسِل
      </a>
    </td>
  </tr>

  <!-- Footer -->
  <tr>
    <td style="background:#2a2a2a;padding:14px 32px;">
      <table width="100%" cellpadding="0" cellspacing="0"><tr>
        <td style="color:#888888;font-size:11px;">© {date.today().year} مخيم الأقصى — جميع الحقوق محفوظة</td>
        <td style="color:#666666;font-size:11px;text-align:left;">هذا بريد آلي — لا تُرسِل رداً على هذا العنوان</td>
      </tr></table>
    </td>
  </tr>

</table>
</td></tr></table>
</body>
</html>
"""
            msg = EmailMultiAlternatives(
                subject=f'[مخيم الأقصى] رسالة جديدة: {subject}',
                body=plain_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send(fail_silently=True)

            messages.success(request, 'وصلت رسالتك — سنرد عليك خلال 24 ساعة في أيام العمل.')
            return redirect('contact')
    return render(request, 'camp/contact.html', {
        'errors': errors,
        'form_data': form_data,
        'contact_info': CONTACT_INFO,
        'subject_choices': SUBJECT_CHOICES,
        'faqs': CONTACT_FAQS,
    })


DONATE_FAQS = [
    {'q': 'هل تبرعي آمن وسري تماماً؟', 'a': 'نعم، نلتزم بسياسة خصوصية صارمة. بياناتك لا تُشارك مع أي طرف ثالث.'},
    {'q': 'كيف سأعرف أين ذهب تبرعي؟', 'a': 'نرسل لك تأكيداً فورياً لكل تبرع، ونصدر تقارير شفافية دورية.'},
    {'q': 'هل يمكنني تبرع مبلغ محدد حسب اختياري؟', 'a': 'بالتأكيد! يمكنك إدخال أي مبلغ يناسبك ابتداءً من دولار واحد.'},
    {'q': 'ماذا لو كنت خارج البلد؟', 'a': 'يمكن التبرع من أي مكان في العالم. المبلغ يُحول بالدولار الأمريكي.'},
]

DONATE_IMPACT = [
    {
        'label': 'الإيواء',
        'desc': 'توفير خيام وملاجئ آمنة',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8"><path d="M3.5 21L14 3"/><path d="M20.5 21L10 3"/><path d="M15.5 21L12 15l-3.5 6"/><path d="M2 21h20"/></svg>',
    },
    {
        'label': 'الغذاء',
        'desc': 'وجبات يومية للعائلات',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8"><path d="M12 6.528V3a1 1 0 0 1 1-1"/><path d="M18.237 21A15 15 0 0 0 22 11a6 6 0 0 0-10-4.472A6 6 0 0 0 2 11a15.1 15.1 0 0 0 3.763 10 3 3 0 0 0 3.648.648 5.5 5.5 0 0 1 5.178 0A3 3 0 0 0 18.237 21"/></svg>',
    },
    {
        'label': 'الصحة',
        'desc': 'رعاية طبية ودوائية',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8"><path d="M12 7v4"/><path d="M14 21v-3a2 2 0 0 0-4 0v3"/><path d="M14 9h-4"/><path d="M18 11h2a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h2"/><path d="M18 21V5a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16"/></svg>',
    },
    {
        'label': 'التعليم',
        'desc': 'فصول دراسية للأطفال',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8"><path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/></svg>',
    },
]


def donate(request):
    story_id = request.GET.get('story')
    story_title = request.GET.get('title', '')[:200].strip()
    story = None
    if story_id:
        story = Article.objects.filter(
            pk=story_id, content_type=Article.STORY, is_published=True
        ).first()
        if story and not story_title:
            story_title = story.title

    errors = {}
    form_data = {}
    if request.method == 'POST':
        form_data = request.POST
        errors = Donation.objects.donation_validator(request.POST)
        if not errors:
            is_anonymous = request.POST.get('is_anonymous') == 'on'
            Donation.objects.create(
                amount=float(request.POST.get('amount', 0)),
                name='متبرع مجهول' if is_anonymous else request.POST.get('name', '').strip(),
                email='' if is_anonymous else request.POST.get('email', '').strip(),
                message='' if is_anonymous else request.POST.get('message', '').strip(),
                is_anonymous=is_anonymous,
                story=story,
            )
            messages.success(request, 'شكراً لتبرعك الكريم — تم تسجيل تبرعك وسيصل أثره مباشرةً.')
            return redirect('/donate/')

    return render(request, 'camp/donate.html', {
        'errors': errors,
        'form_data': form_data,
        'story': story,
        'story_title': story_title,
        'faqs': DONATE_FAQS,
        'impact': DONATE_IMPACT,
        'quick_amounts': [10, 25, 50, 100, 250],
    })


def home(request):
    hero_slides = list(HeroSlide.objects.filter(is_active=True)[:3])
    statistics = list(SiteStatistic.objects.all()[:4])
    services = list(Service.objects.filter(is_active=True))
    for svc in services:
        svc.icon_svg = SERVICE_ICONS.get(svc.icon_name, SERVICE_ICONS['default'])
    for stat in statistics:
        stat.icon_svg = SERVICE_ICONS.get(stat.icon_name, SERVICE_ICONS['default'])
    return render(request, 'camp/home.html', {
        'hero_slides': hero_slides,
        'statistics': statistics,
        'services': services,
        'mission_values': MISSION_VALUES,
        'islamic_quote': ISLAMIC_QUOTE,
    })
