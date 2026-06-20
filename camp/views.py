from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Article, Donation, HeroSlide, SiteStatistic, Service

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
            messages.success(request, 'شكراً لتبرعك الكريم! تم تسجيل تبرعك بنجاح.')
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
    return render(request, 'camp/home.html', {
        'hero_slides': hero_slides,
        'statistics': statistics,
        'services': services,
        'mission_values': MISSION_VALUES,
        'islamic_quote': ISLAMIC_QUOTE,
    })
