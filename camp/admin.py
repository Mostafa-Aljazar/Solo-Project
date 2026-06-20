from django.contrib import admin
from .models import Article, HeroSlide, SiteStatistic, Service


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'is_published', 'created_at']
    list_filter = ['content_type', 'is_published']
    search_fields = ['title', 'brief']


admin.site.register(HeroSlide)
admin.site.register(SiteStatistic)
admin.site.register(Service)
