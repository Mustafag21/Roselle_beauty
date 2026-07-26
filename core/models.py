"""
Roselle Beauty & Care — Veritabanı Modelleri (Tam Yeniden Tasarım)
Tüm site içeriği admin panelinden yönetilir.
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils import timezone


# ──────────────────────────────────────────────────────────────
# SITE AYARLARI (Singleton)
# ──────────────────────────────────────────────────────────────
class SiteSettings(models.Model):
    site_title = models.CharField('Site Başlığı', max_length=200, default='Roselle Beauty & Care')
    site_slogan = models.CharField('Site Sloganı', max_length=300, blank=True, default='Cildinize Değer Katın')
    logo = models.ImageField('Logo', upload_to='site/', blank=True, null=True)
    logo_light = models.ImageField('Logo (Açık/Beyaz)', upload_to='site/', blank=True, null=True,
        help_text='Footer ve koyu arka plan için açık renkli logo')
    favicon = models.ImageField('Favicon', upload_to='site/', blank=True, null=True)
    meta_description = models.TextField('Meta Açıklama', blank=True,
        default='Roselle Beauty & Care — Doğal güzelliğinizi keşfedin. Profesyonel cilt ve saç bakım ürünleri.')
    meta_keywords = models.CharField('Anahtar Kelimeler', max_length=500, blank=True,
        default='roselle beauty, cilt bakım, saç bakım, serum, doğal kozmetik')
    footer_text = models.TextField('Footer Metni', blank=True,
        default='© 2024 Roselle Beauty & Care. Tüm hakları saklıdır.')
    footer_description = models.TextField('Footer Açıklama', blank=True,
        default='Doğal ve etkili formüllerle cildinize ve saçlarınıza değer katıyoruz.')
    whatsapp_number = models.CharField('WhatsApp Numarası', max_length=20, blank=True,
        help_text='Uluslararası format: 905551234567')
    whatsapp_default_message = models.CharField('WhatsApp Varsayılan Mesaj', max_length=500, blank=True,
        default='Merhaba, ürünleriniz hakkında bilgi almak istiyorum.')
    google_reviews_widget_code = models.TextField('Google Yorumlar Widget Kodu', blank=True,
        help_text='Elfsight, Trustpilot veya benzeri platformlardan aldığınız embed kodunu buraya yapıştırın. Bu kod aktifse, sitemizdeki yorumlar kısmında gösterilecektir.')

    class Meta:
        verbose_name = 'Site Ayarları'
        verbose_name_plural = 'Site Ayarları'

    def __str__(self):
        return self.site_title

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('Sadece bir kayıt oluşturulabilir.')
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ──────────────────────────────────────────────────────────────
# HERO / BANNER BÖLÜMLERİ
# ──────────────────────────────────────────────────────────────
class HeroBanner(models.Model):
    title = models.CharField('Başlık', max_length=200)
    subtitle = models.TextField('Alt Başlık', blank=True)
    background_image = models.ImageField('Arka Plan Görseli', upload_to='hero/')
    cta_text = models.CharField('Buton Metni', max_length=100, blank=True, default='Keşfet')
    cta_link = models.CharField('Buton Bağlantısı', max_length=200, blank=True, default='/urunler/')
    overlay_opacity = models.PositiveIntegerField('Overlay Opaklığı (%)', default=40,
        help_text='0-100 arası. Metnin okunabilirliği için arka plan kararma oranı.')
    is_active = models.BooleanField('Aktif', default=True)
    order = models.PositiveIntegerField('Sıra', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Hero Banner'
        verbose_name_plural = 'Hero Bannerlar'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────────────────────
# ÜRÜN KATEGORİLERİ & ÜRÜNLER
# ──────────────────────────────────────────────────────────────
class ProductCategory(models.Model):
    name = models.CharField('Kategori Adı', max_length=100)
    slug = models.SlugField('URL Slug', unique=True, blank=True)
    description = models.TextField('Açıklama', blank=True)
    icon = models.CharField('İkon CSS Sınıfı', max_length=50, blank=True,
        help_text='Font Awesome ikon sınıfı (ör: fas fa-leaf)')
    image = models.ImageField('Kategori Görseli', upload_to='categories/', blank=True, null=True)
    order = models.PositiveIntegerField('Sıra', default=0)
    is_active = models.BooleanField('Aktif', default=True)

    class Meta:
        verbose_name = 'Ürün Kategorisi'
        verbose_name_plural = 'Ürün Kategorileri'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def active_product_count(self):
        return self.products.filter(is_active=True).count()


class Product(models.Model):
    BADGE_CHOICES = [
        ('', 'Badge Yok'),
        ('yeni', 'Yeni'),
        ('cok-satan', 'Çok Satan'),
        ('indirim', 'İndirimli'),
        ('ozel', 'Özel Ürün'),
    ]
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Kategori', related_name='products')
    name = models.CharField('Ürün Adı', max_length=200)
    slug = models.SlugField('URL Slug', unique=True, blank=True)
    short_description = models.CharField('Kısa Açıklama', max_length=300,
        help_text='Ürün kartında görünecek kısa açıklama')
    description = models.TextField('Detaylı Açıklama')
    ingredients = models.TextField('İçerik Bilgisi', blank=True)
    usage_info = models.TextField('Kullanım Bilgisi', blank=True)
    volume = models.CharField('Hacim/Boyut', max_length=50, blank=True, help_text='Ör: 50 ML / 1.69 fl.oz.')
    image = models.ImageField('Ana Görsel', upload_to='products/')
    image_hover = models.ImageField('Hover Görseli', upload_to='products/', blank=True, null=True,
        help_text='Ürün kartında fare üzerine gelince gösterilecek görsel')
    badge = models.CharField('Rozet', max_length=20, choices=BADGE_CHOICES, blank=True, default='')
    dominant_color = models.CharField('Tema Rengi', max_length=7, default='#B8956A',
        help_text='Ürün kartında accent renk olarak kullanılacak (HEX)')
    is_featured = models.BooleanField('Öne Çıkan', default=False)
    is_active = models.BooleanField('Aktif', default=True)
    order = models.PositiveIntegerField('Sıra', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ürün'
        verbose_name_plural = 'Ürünler'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Ürün için ek görseller (galeri)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images',
        verbose_name='Ürün')
    image = models.ImageField('Görsel', upload_to='products/gallery/')
    alt_text = models.CharField('Alt Metin', max_length=200, blank=True)
    order = models.PositiveIntegerField('Sıra', default=0)

    class Meta:
        verbose_name = 'Ürün Görseli'
        verbose_name_plural = 'Ürün Görselleri'
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} — Görsel #{self.order}"


# ──────────────────────────────────────────────────────────────
# HİZMETLER
# ──────────────────────────────────────────────────────────────
class Service(models.Model):
    name = models.CharField('Hizmet Adı', max_length=200)
    slug = models.SlugField('URL Slug', unique=True, blank=True)
    short_description = models.CharField('Kısa Açıklama', max_length=300)
    description = models.TextField('Detaylı Açıklama', blank=True)
    image = models.ImageField('Hizmet Görseli', upload_to='services/')
    icon = models.CharField('İkon', max_length=50, blank=True, default='fas fa-spa')
    is_active = models.BooleanField('Aktif', default=True)
    order = models.PositiveIntegerField('Sıra', default=0)

    class Meta:
        verbose_name = 'Hizmet'
        verbose_name_plural = 'Hizmetler'
        ordering = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ──────────────────────────────────────────────────────────────
# BLOG
# ──────────────────────────────────────────────────────────────
class BlogCategory(models.Model):
    name = models.CharField('Kategori Adı', max_length=100)
    slug = models.SlugField('URL Slug', unique=True, blank=True)
    order = models.PositiveIntegerField('Sıra', default=0)

    class Meta:
        verbose_name = 'Blog Kategorisi'
        verbose_name_plural = 'Blog Kategorileri'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Kategori', related_name='posts')
    title = models.CharField('Başlık', max_length=300)
    slug = models.SlugField('URL Slug', unique=True, blank=True)
    excerpt = models.TextField('Özet', max_length=500,
        help_text='Blog listesinde görünecek kısa özet')
    content = models.TextField('İçerik')
    cover_image = models.ImageField('Kapak Görseli', upload_to='blog/')
    author = models.CharField('Yazar', max_length=100, default='Roselle Beauty')
    read_time = models.PositiveIntegerField('Okuma Süresi (dk)', default=5)
    is_published = models.BooleanField('Yayınlandı', default=True)
    is_featured = models.BooleanField('Öne Çıkan', default=False)
    meta_description = models.TextField('SEO Açıklama', blank=True)
    published_at = models.DateTimeField('Yayın Tarihi', default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Blog Yazısı'
        verbose_name_plural = 'Blog Yazıları'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        super().save(*args, **kwargs)


# ──────────────────────────────────────────────────────────────
# HAKKIMIZDA (Singleton)
# ──────────────────────────────────────────────────────────────
class AboutSection(models.Model):
    title = models.CharField('Başlık', max_length=200, default='Hakkımızda')
    subtitle = models.CharField('Alt Başlık', max_length=300, blank=True,
        default='Doğal güzelliğinizi keşfedin')
    content = models.TextField('Ana İçerik',
        default='Roselle Beauty & Care olarak doğal ve etkili formüllerle cildinize ve saçlarınıza değer katıyoruz.')
    image = models.ImageField('Ana Görsel', upload_to='about/', blank=True, null=True)
    mission = models.TextField('Misyonumuz', blank=True)
    vision = models.TextField('Vizyonumuz', blank=True)
    story = models.TextField('Hikayemiz', blank=True,
        help_text='Markanın kuruluş hikayesi')
    years_experience = models.PositiveIntegerField('Yıl Deneyim', default=5)
    happy_customers = models.PositiveIntegerField('Mutlu Müşteri', default=10000)
    products_count = models.PositiveIntegerField('Ürün Sayısı', default=20)
    natural_ingredients = models.PositiveIntegerField('Doğal İçerik (%)', default=95)

    class Meta:
        verbose_name = 'Hakkımızda'
        verbose_name_plural = 'Hakkımızda'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and AboutSection.objects.exists():
            raise ValidationError('Sadece bir kayıt oluşturulabilir.')
        super().save(*args, **kwargs)

    @classmethod
    def get_about(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ──────────────────────────────────────────────────────────────
# SSS (FAQ)
# ──────────────────────────────────────────────────────────────
class FAQ(models.Model):
    question = models.CharField('Soru', max_length=500)
    answer = models.TextField('Cevap')
    order = models.PositiveIntegerField('Sıra', default=0)
    is_active = models.BooleanField('Aktif', default=True)

    class Meta:
        verbose_name = 'Sık Sorulan Soru'
        verbose_name_plural = 'Sık Sorulan Sorular'
        ordering = ['order']

    def __str__(self):
        return self.question[:80]


# ──────────────────────────────────────────────────────────────
# İLETİŞİM BİLGİLERİ (Singleton)
# ──────────────────────────────────────────────────────────────
class ContactInfo(models.Model):
    address = models.TextField('Adres', default='İstanbul, Türkiye')
    phone = models.CharField('Telefon', max_length=20, default='+90 555 123 4567')
    email = models.EmailField('E-posta', default='info@rosellebeauty.com')
    whatsapp = models.CharField('WhatsApp Numarası', max_length=20, blank=True,
        help_text='Uluslararası format: 905551234567')
    map_embed = models.TextField('Google Maps Embed Kodu', blank=True)
    map_link = models.URLField('Google Maps Bağlantısı', blank=True)
    working_hours_weekday = models.CharField('Hafta İçi', max_length=50, default='09:00 - 21:00')
    working_hours_saturday = models.CharField('Cumartesi', max_length=50, default='10:00 - 20:00')
    working_hours_sunday = models.CharField('Pazar', max_length=50, default='Kapalı')

    class Meta:
        verbose_name = 'İletişim Bilgileri'
        verbose_name_plural = 'İletişim Bilgileri'

    def __str__(self):
        return f"İletişim — {self.phone}"

    def save(self, *args, **kwargs):
        if not self.pk and ContactInfo.objects.exists():
            raise ValidationError('Sadece bir kayıt oluşturulabilir.')
        super().save(*args, **kwargs)

    @classmethod
    def get_contact(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ──────────────────────────────────────────────────────────────
# SOSYAL MEDYA
# ──────────────────────────────────────────────────────────────
class SocialMedia(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('whatsapp', 'WhatsApp'),
        ('google_business', 'Google İşletme'),
        ('facebook', 'Facebook'),
        ('twitter', 'X (Twitter)'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('linkedin', 'LinkedIn'),
    ]
    ICON_MAP = {
        'instagram': 'fab fa-instagram',
        'whatsapp': 'fab fa-whatsapp',
        'google_business': 'fab fa-google',
        'facebook': 'fab fa-facebook-f',
        'twitter': 'fab fa-x-twitter',
        'youtube': 'fab fa-youtube',
        'tiktok': 'fab fa-tiktok',
        'linkedin': 'fab fa-linkedin-in',
    }
    platform = models.CharField('Platform', max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField('Bağlantı URL')
    is_active = models.BooleanField('Aktif', default=True)
    order = models.PositiveIntegerField('Sıra', default=0)

    class Meta:
        verbose_name = 'Sosyal Medya'
        verbose_name_plural = 'Sosyal Medya'
        ordering = ['order']

    def __str__(self):
        return self.get_platform_display()

    @property
    def icon_class(self):
        return self.ICON_MAP.get(self.platform, 'fas fa-link')


# ──────────────────────────────────────────────────────────────
# İLETİŞİM MESAJLARI
# ──────────────────────────────────────────────────────────────
class ContactMessage(models.Model):
    name = models.CharField('Ad Soyad', max_length=100)
    email = models.EmailField('E-posta')
    phone = models.CharField('Telefon', max_length=20, blank=True)
    subject = models.CharField('Konu', max_length=200)
    message = models.TextField('Mesaj')
    created_at = models.DateTimeField('Gönderilme', auto_now_add=True)
    is_read = models.BooleanField('Okundu', default=False)

    class Meta:
        verbose_name = 'İletişim Mesajı'
        verbose_name_plural = 'İletişim Mesajları'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.subject}"


# ──────────────────────────────────────────────────────────────
# MÜŞTERİ YORUMLARI
# ──────────────────────────────────────────────────────────────
class Testimonial(models.Model):
    name = models.CharField('Müşteri Adı', max_length=100)
    role = models.CharField('Ünvan/Meslek', max_length=100, blank=True)
    text = models.TextField('Yorum')
    rating = models.PositiveIntegerField('Puan', default=5,
        help_text='1-5 arası puan')
    photo = models.ImageField('Fotoğraf', upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField('Aktif', default=True)
    order = models.PositiveIntegerField('Sıra', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Müşteri Yorumu'
        verbose_name_plural = 'Müşteri Yorumları'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} — {'⭐' * self.rating}"


# ──────────────────────────────────────────────────────────────
# NEWSLETTER
# ──────────────────────────────────────────────────────────────
class Newsletter(models.Model):
    email = models.EmailField('E-posta', unique=True)
    subscribed_at = models.DateTimeField('Kayıt Tarihi', auto_now_add=True)
    is_active = models.BooleanField('Aktif', default=True)

    class Meta:
        verbose_name = 'Bülten Abonesi'
        verbose_name_plural = 'Bülten Aboneleri'
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


# ──────────────────────────────────────────────────────────────
# GALERİ
# ──────────────────────────────────────────────────────────────
class GalleryImage(models.Model):
    title = models.CharField('Başlık', max_length=200, blank=True)
    image = models.ImageField('Görsel', upload_to='gallery/')
    description = models.TextField('Açıklama', blank=True)
    order = models.PositiveIntegerField('Sıra', default=0)
    is_active = models.BooleanField('Aktif', default=True)

    class Meta:
        verbose_name = 'Galeri Görseli'
        verbose_name_plural = 'Galeri Görselleri'
        ordering = ['order']

    def __str__(self):
        return self.title or f"Görsel #{self.pk}"


# ──────────────────────────────────────────────────────────────
# MARKA İSTATİSTİK BANDI (Brand Ticker)
# ──────────────────────────────────────────────────────────────
class BrandFeature(models.Model):
    """Ana sayfadaki özellik bandı için (Doğal İçerik, Dermatolog Onaylı vb.)"""
    text = models.CharField('Metin', max_length=100)
    icon = models.CharField('İkon', max_length=50, blank=True, default='fas fa-check')
    order = models.PositiveIntegerField('Sıra', default=0)
    is_active = models.BooleanField('Aktif', default=True)

    class Meta:
        verbose_name = 'Marka Özelliği'
        verbose_name_plural = 'Marka Özellikleri'
        ordering = ['order']

    def __str__(self):
        return self.text
