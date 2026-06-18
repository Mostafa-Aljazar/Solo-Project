from django.shortcuts import render
from .models import HeroSlide, SiteStatistic, Service

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
