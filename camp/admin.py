from django.contrib import admin
from .models import Article, Donation, ContactMessage, HeroSlide, SiteStatistic, Service


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'is_published', 'created_at']
    list_filter = ['content_type', 'is_published']
    search_fields = ['title', 'brief']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'amount', 'is_anonymous', 'story', 'created_at']
    list_filter = ['is_anonymous']
    readonly_fields = ['amount', 'name', 'email', 'message', 'is_anonymous', 'story', 'created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['subject']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(HeroSlide)
admin.site.register(SiteStatistic)
admin.site.register(Service)
