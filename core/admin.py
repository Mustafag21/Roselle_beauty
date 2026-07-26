"""
Roselle Beauty & Care — Admin Panel (Tam Yeniden Tasarım)
Tüm site içeriği buradan yönetilir.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, HeroBanner, ProductCategory, Product, ProductImage,
    Service, BlogCategory, BlogPost, AboutSection, FAQ, ContactInfo,
    SocialMedia, ContactMessage, Testimonial, Newsletter, GalleryImage,
    BrandFeature,
)


# ──────────────────────────────────────────────────────────────
# INLINE MODELLER
# ──────────────────────────────────────────────────────────────
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" style="border-radius:8px;"/>', obj.image.url)
        return "—"
    image_preview.short_description = 'Önizleme'


# ──────────────────────────────────────────────────────────────
# SİTE AYARLARI
# ──────────────────────────────────────────────────────────────
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_title', 'site_slogan', 'logo_preview']
    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('site_title', 'site_slogan'),
        }),
        ('Logo & Favicon', {
            'fields': ('logo', 'logo_light', 'favicon'),
            'description': 'Koyu arka plan (footer vb.) için ayrı bir açık renkli logo yükleyebilirsiniz.',
        }),
        ('SEO Ayarları', {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        ('WhatsApp Ayarları', {
            'fields': ('whatsapp_number', 'whatsapp_default_message'),
            'description': 'Ürün kartlarındaki "İletişime Geç" butonu bu numaraya yönlendirecektir.',
        }),
        ('Harici Entegrasyonlar (Widget)', {
            'fields': ('google_reviews_widget_code',),
            'description': 'Elfsight veya Trustpilot gibi sitelerden aldığınız Google Yorumlar embed kodunu buraya yapıştırabilirsiniz.',
        }),
        ('Footer', {
            'fields': ('footer_text', 'footer_description'),
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" height="40" style="border-radius:4px;"/>', obj.logo.url)
        return "—"
    logo_preview.short_description = 'Logo'

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ──────────────────────────────────────────────────────────────
# HERO BANNER
# ──────────────────────────────────────────────────────────────
@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'title', 'cta_text', 'is_active', 'order']
    list_display_links = ['title']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    fieldsets = (
        ('İçerik', {'fields': ('title', 'subtitle', 'background_image')}),
        ('Buton', {'fields': ('cta_text', 'cta_link')}),
        ('Ayarlar', {'fields': ('overlay_opacity', 'is_active', 'order')}),
    )

    def image_preview(self, obj):
        if obj.background_image:
            return format_html(
                '<img src="{}" height="50" style="border-radius:8px;object-fit:cover;width:90px;"/>',
                obj.background_image.url
            )
        return "—"
    image_preview.short_description = 'Görsel'


# ──────────────────────────────────────────────────────────────
# ÜRÜN KATEGORİLERİ
# ──────────────────────────────────────────────────────────────
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return obj.active_product_count
    product_count.short_description = 'Ürün Sayısı'


# ──────────────────────────────────────────────────────────────
# ÜRÜNLER
# ──────────────────────────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category', 'badge',
                    'color_preview', 'is_featured', 'is_active', 'order']
    list_display_links = ['name']
    list_editable = ['is_featured', 'is_active', 'order']
    list_filter = ['category', 'is_featured', 'is_active', 'badge']
    search_fields = ['name', 'short_description', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'slug', 'category', 'badge', 'volume'),
        }),
        ('Görseller', {
            'fields': ('image', 'image_hover'),
            'description': 'Ana görsel ve fare üzerine gelince gösterilecek ikinci görsel.',
        }),
        ('Açıklamalar', {
            'fields': ('short_description', 'description', 'ingredients', 'usage_info'),
        }),
        ('Tasarım', {
            'fields': ('dominant_color',),
        }),
        ('Ayarlar', {
            'fields': ('is_featured', 'is_active', 'order'),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" height="50" style="border-radius:8px;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = 'Görsel'



    def color_preview(self, obj):
        return format_html(
            '<div style="width:24px;height:24px;border-radius:50%;background:{};'
            'border:2px solid #ddd;"></div>', obj.dominant_color
        )
    color_preview.short_description = 'Renk'


# ──────────────────────────────────────────────────────────────
# HİZMETLER
# ──────────────────────────────────────────────────────────────
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'is_active', 'order']
    list_display_links = ['name']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Temel', {'fields': ('name', 'slug', 'icon', 'image')}),
        ('Açıklamalar', {'fields': ('short_description', 'description')}),
        ('Ayarlar', {'fields': ('is_active', 'order')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" height="50" style="border-radius:8px;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = 'Görsel'


# ──────────────────────────────────────────────────────────────
# BLOG
# ──────────────────────────────────────────────────────────────
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.filter(is_published=True).count()
    post_count.short_description = 'Yazı Sayısı'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['cover_preview', 'title', 'category', 'author', 'published_at',
                    'is_published', 'is_featured']
    list_display_links = ['title']
    list_editable = ['is_published', 'is_featured']
    list_filter = ['category', 'is_published', 'is_featured']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'category', 'author', 'cover_image'),
        }),
        ('İçerik', {
            'fields': ('excerpt', 'content'),
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',),
        }),
        ('Ayarlar', {
            'fields': ('read_time', 'is_published', 'is_featured', 'published_at'),
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" height="50" style="border-radius:8px;object-fit:cover;width:80px;"/>',
                obj.cover_image.url
            )
        return "—"
    cover_preview.short_description = 'Kapak'


# ──────────────────────────────────────────────────────────────
# HAKKIMIZDA
# ──────────────────────────────────────────────────────────────
@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('İçerik', {'fields': ('title', 'subtitle', 'content', 'image')}),
        ('Hikaye & Vizyon', {'fields': ('story', 'mission', 'vision')}),
        ('İstatistikler', {
            'fields': ('years_experience', 'happy_customers', 'products_count', 'natural_ingredients'),
            'description': 'Ana sayfada gösterilecek sayısal veriler.',
        }),
    )

    def has_add_permission(self, request):
        return not AboutSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ──────────────────────────────────────────────────────────────
# SSS
# ──────────────────────────────────────────────────────────────
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_short', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']

    def question_short(self, obj):
        return obj.question[:80]
    question_short.short_description = 'Soru'


# ──────────────────────────────────────────────────────────────
# İLETİŞİM BİLGİLERİ
# ──────────────────────────────────────────────────────────────
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('İletişim', {'fields': ('phone', 'email', 'whatsapp')}),
        ('Adres & Harita', {'fields': ('address', 'map_embed', 'map_link')}),
        ('Çalışma Saatleri', {
            'fields': ('working_hours_weekday', 'working_hours_saturday', 'working_hours_sunday'),
        }),
    )

    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ──────────────────────────────────────────────────────────────
# SOSYAL MEDYA
# ──────────────────────────────────────────────────────────────
@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['platform_icon', 'platform', 'url_short', 'is_active', 'order']
    list_display_links = ['platform']
    list_editable = ['is_active', 'order']
    list_filter = ['platform', 'is_active']

    def platform_icon(self, obj):
        return format_html('<i class="{}"></i>', obj.icon_class)
    platform_icon.short_description = 'İkon'

    def url_short(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url[:50])
    url_short.short_description = 'Bağlantı'


# ──────────────────────────────────────────────────────────────
# İLETİŞİM MESAJLARI
# ──────────────────────────────────────────────────────────────
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'phone', 'created_at', 'is_read']
    list_display_links = ['name', 'subject']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False


# ──────────────────────────────────────────────────────────────
# MÜŞTERİ YORUMLARI
# ──────────────────────────────────────────────────────────────
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['photo_preview', 'name', 'role', 'rating_stars', 'is_active', 'order']
    list_display_links = ['name']
    list_editable = ['is_active', 'order']
    list_filter = ['rating', 'is_active']

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" height="40" style="border-radius:50%;width:40px;object-fit:cover;"/>',
                obj.photo.url
            )
        return format_html(
            '<div style="width:40px;height:40px;border-radius:50%;background:#C4707E;'
            'display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;">'
            '{}</div>', obj.name[0].upper()
        )
    photo_preview.short_description = 'Foto'

    def rating_stars(self, obj):
        return '⭐' * obj.rating
    rating_stars.short_description = 'Puan'


# ──────────────────────────────────────────────────────────────
# NEWSLETTER
# ──────────────────────────────────────────────────────────────
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']
    date_hierarchy = 'subscribed_at'

    def has_add_permission(self, request):
        return False


# ──────────────────────────────────────────────────────────────
# GALERİ
# ──────────────────────────────────────────────────────────────
@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" height="50" style="border-radius:8px;object-fit:cover;width:80px;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = 'Görsel'


# ──────────────────────────────────────────────────────────────
# MARKA ÖZELLİKLERİ
# ──────────────────────────────────────────────────────────────
@admin.register(BrandFeature)
class BrandFeatureAdmin(admin.ModelAdmin):
    list_display = ['text', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
