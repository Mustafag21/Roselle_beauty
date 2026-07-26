import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roselle_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import (
    SiteSettings, HeroBanner, ProductCategory, Product, ProductImage,
    Service, BlogCategory, BlogPost, AboutSection, FAQ, ContactInfo,
    SocialMedia, Testimonial, GalleryImage, BrandFeature
)

def seed():
    print("Database seeding started...")

    # 1. Superuser
    User.objects.filter(username='admin').delete()
    User.objects.create_superuser('admin', 'admin@example.com', 'roselle.21')
    print("Superuser 'admin' created/reset.")

    # Create media subfolders
    media_paths = [
        'media/site', 'media/products', 'media/products/gallery',
        'media/hero', 'media/about', 'media/services',
        'media/blog', 'media/testimonials', 'media/gallery'
    ]
    for path in media_paths:
        os.makedirs(os.path.join('/Users/gulcu.21/Desktop/roselle_beauty', path), exist_ok=True)

    assets_src = '/Users/gulcu.21/Desktop/roselle_beauty/Ürünler ve Reklamlar'
    media_dest = '/Users/gulcu.21/Desktop/roselle_beauty/media'

    # Helper function to copy image safely
    def copy_media(src_name, dest_subpath):
        src_path = os.path.join(assets_src, src_name)
        dest_path = os.path.join(media_dest, dest_subpath)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            return dest_subpath
        return None

    # Copy logo
    logo_path = copy_media('WhatsApp Image 2026-04-14 at 13.42.17.jpeg', 'site/logo.jpeg')
    logo_light_path = copy_media('WhatsApp Image 2026-04-14 at 13.42.17.jpeg', 'site/logo_light.jpeg')

    # Copy banners
    copy_media('30.jpeg', 'hero/banner1.jpeg')
    copy_media('28.jpeg', 'hero/banner2.jpeg')

    # Copy about image
    copy_media('29.jpeg', 'about/about_main.jpeg')

    # Copy product images
    copy_media('1.jpeg', 'products/sac_serumu.jpeg')
    copy_media('0.jpeg', 'products/sac_serumu_hover.jpeg')
    copy_media('2.jpeg', 'products/gallery/sac_serumu_ad.jpeg')

    copy_media('5.jpeg', 'products/sac_yagi.jpeg')
    copy_media('3.jpeg', 'products/sac_yagi_hover.jpeg')
    copy_media('4.jpeg', 'products/gallery/sac_yagi_ad.jpeg')

    copy_media('6.jpeg', 'products/anti_aging.jpeg')
    copy_media('8.jpeg', 'products/anti_aging_hover.jpeg')
    copy_media('7.jpeg', 'products/gallery/anti_aging_ad.jpeg')

    copy_media('15.jpeg', 'products/leke_serumu.jpeg')

    copy_media('11.jpeg', 'products/vitamin_c.jpeg')
    copy_media('9.jpeg', 'products/vitamin_c_hover.jpeg')
    copy_media('10.jpeg', 'products/gallery/vitamin_c_ad.jpeg')

    copy_media('20.jpeg', 'products/kolajen_serum.jpeg')
    copy_media('25.jpeg', 'products/retinol_serum.jpeg')

    copy_media('13.jpeg', 'products/peeling_serum.jpeg')
    copy_media('12.jpeg', 'products/peeling_serum_hover.jpeg')
    copy_media('14.jpeg', 'products/gallery/peeling_serum_ad.jpeg')

    # Copy all other images to gallery
    for i in range(31):
        filename = f"{i}.jpeg"
        copy_media(filename, f"gallery/{filename}")

    print("Media assets copied successfully.")

    # 2. Site Settings
    SiteSettings.objects.all().delete()
    site = SiteSettings.objects.create(
        site_title="Roselle Beauty & Care",
        site_slogan="Cildinize Değer Katın",
        logo=logo_path,
        logo_light=logo_light_path,
        meta_description="Roselle Beauty & Care — Doğal güzelliğinizi keşfedin. Profesyonel cilt ve saç bakım ürünleri.",
        meta_keywords="roselle beauty, cilt bakım, saç bakım, serum, doğal kozmetik",
        footer_text="© 2024 Roselle Beauty & Care. Tüm hakları saklıdır.",
        footer_description="Doğal ve etkili formüllerle cildinize ve saçlarınıza değer katıyoruz.",
        whatsapp_number="905551234567",
        whatsapp_default_message="Merhaba, Roselle ürünleriniz hakkında bilgi almak istiyorum."
    )
    print("Site settings seeded.")

    # 3. Hero Banners
    HeroBanner.objects.all().delete()
    HeroBanner.objects.create(
        title="Güzelliğinize Değer Katın",
        subtitle="Doğal bitki özleri ve bilimsel formüllerle saç ve cilt bakımında yeni bir çağ.",
        background_image="hero/banner1.jpeg",
        cta_text="Ürünlerimizi Keşfedin",
        cta_link="/urunler/",
        overlay_opacity=50,
        order=1
    )
    HeroBanner.objects.create(
        title="Işıltınızı Yeniden Keşfedin",
        subtitle="Yaşlanma karşıtı altın formüllerimiz ile cildiniz her an taze ve pürüzsüz.",
        background_image="hero/banner2.jpeg",
        cta_text="Blog Yazılarımızı Oku",
        cta_link="/blog/",
        overlay_opacity=45,
        order=2
    )
    print("Hero banners seeded.")

    # 4. Brand Features
    BrandFeature.objects.all().delete()
    BrandFeature.objects.create(text="Doğal İçerik", icon="fas fa-leaf", order=1)
    BrandFeature.objects.create(text="Dermatolojik Olarak Test Edildi", icon="fas fa-user-md", order=2)
    BrandFeature.objects.create(text="Vegan Formül", icon="fas fa-seedling", order=3)
    BrandFeature.objects.create(text="Hayvanlar Üzerinde Deney Yapılmaz", icon="fas fa-paw", order=4)
    print("Brand features seeded.")

    # 5. Categories
    ProductCategory.objects.all().delete()
    cilt_bakim = ProductCategory.objects.create(name="Cilt Bakımı", icon="fas fa-sparkles", order=1)
    sac_bakim = ProductCategory.objects.create(name="Saç Bakımı", icon="fas fa-cut", order=2)
    print("Product categories seeded.")

    # 6. Products
    Product.objects.all().delete()
    
    # Product 1
    sac_serumu = Product.objects.create(
        category=sac_bakim,
        name="Saç Bakım Serumu (Kadın)",
        short_description="Biotin, Keratin ve Procapil içeren saç dökülmesine karşı besleyici serum.",
        description="Roselle Saç Bakım Serumu, kadınlar için özel geliştirilmiş formülüyle saç köklerini besler ve dökülmeleri önlemeye yardımcı olur. Saçın daha gür, canlı ve parlak çıkmasını destekler.",
        ingredients="Procapil (%3-%5), Biotin (Vitamin B7), Keratin, At Kuyruğu Özü, Bitkisel Kompleksler.",
        usage_info="Temiz kafa derisine dairesel hareketlerle masaj yaparak uygulayınız. Durulama gerektirmez. Günde 1 defa kullanılması tavsiye edilir.",
        volume="50 ML / 1.69 fl.oz.",
        image="products/sac_serumu.jpeg",
        image_hover="products/sac_serumu_hover.jpeg",
        price=349.90,
        badge="cok-satan",
        dominant_color="#B8857A",
        is_featured=True,
        order=1
    )
    ProductImage.objects.create(product=sac_serumu, image="products/gallery/sac_serumu_ad.jpeg", alt_text="Saç Serumu Özellikleri", order=1)

    # Product 2
    sac_yagi = Product.objects.create(
        category=sac_bakim,
        name="Besleyici Saç Bakım Yağı",
        short_description="Argan, Jojoba ve Hindistan Cevizi yağlarıyla yıpranmış saçlar için yoğun bakım.",
        description="Roselle Besleyici Saç Bakım Yağı, zengin doğal yağ kompleksi ile kuru ve yıpranmış saç tellerinizi derinlemesine nemlendirir. Saçın kabarmasını önler ve ipeksi bir yumuşaklık verir.",
        ingredients="Argan Yağı, Jojoba Yağı, Hindistan Cevizi Yağı, Tatlı Badem Yağı, E Vitamini.",
        usage_info="Avucunuza birkaç damla alarak saç uçlarına ve boylarına eşit şekilde uygulayın. Nemli veya kuru saça uygulanabilir.",
        volume="50 ML / 1.69 fl.oz.",
        image="products/sac_yagi.jpeg",
        image_hover="products/sac_yagi_hover.jpeg",
        price=299.90,
        badge="yeni",
        dominant_color="#B8956A",
        is_featured=True,
        order=2
    )
    ProductImage.objects.create(product=sac_yagi, image="products/gallery/sac_yagi_ad.jpeg", alt_text="Saç Yağı Faydaları", order=1)

    # Product 3
    anti_aging = Product.objects.create(
        category=cilt_bakim,
        name="Anti Aging Kırışıklık Karşıtı Serum",
        short_description="Kolajen ve Aloe Vera ile zenginleştirilmiş sıkılaştırıcı bakım serumu.",
        description="Roselle Anti Aging Serum, ince çizgi ve kırışıklıkların görünümünü azaltmaya yardımcı olur. Kolajen içeriği ile cildin elastikiyetini artırır ve daha sıkı bir görünüm kazandırır.",
        ingredients="Kolajen, Aloe Vera Ekstraktı, C Vitamini, Tokoferil Asetat (E Vitamini), Papatya Özleri.",
        usage_info="Geceleri temizlenmiş yüz ve boyun bölgesine 3-4 damla uygulayın. Yukarı doğru dairesel hareketlerle masaj yapın.",
        volume="30 ML / 1.01 fl.oz.",
        image="products/anti_aging.jpeg",
        image_hover="products/anti_aging_hover.jpeg",
        price=449.90,
        badge="cok-satan",
        dominant_color="#B8857A",
        is_featured=True,
        order=3
    )
    ProductImage.objects.create(product=anti_aging, image="products/gallery/anti_aging_ad.jpeg", alt_text="Anti Aging Özellikleri", order=1)

    # Product 4
    leke_serumu = Product.objects.create(
        category=cilt_bakim,
        name="Leke Karşıtı Niacinamide Serum",
        short_description="Cilt tonunu eşitlemeye ve lekelerin görünümünü azaltmaya yardımcı formül.",
        description="Ciltteki güneş lekeleri, akne izleri ve renk eşitsizlikleri için geliştirilmiş yoğun leke serumudur. Cildin bariyerini güçlendirerek aydınlık bir duruş kazandırır.",
        ingredients="Niasinamid (B3 Vitamini), Alpha-Arbutin, Hyaluronik Asit.",
        usage_info="Temiz cilde sabah ve akşam birkaç damla uygulayın. Gündüz kullanımında güneş kremi kullanılması önemle tavsiye edilir.",
        volume="30 ML / 1.01 fl.oz.",
        image="products/leke_serumu.jpeg",
        price=389.90,
        badge="ozel",
        dominant_color="#7A9E7E",
        is_featured=True,
        order=4
    )

    # Product 5
    vitamin_c = Product.objects.create(
        category=cilt_bakim,
        name="Aydınlatıcı C Vitamini Serumu",
        short_description="Yüksek antioksidan etkili, ışıltı veren C Vitamini cilt bakım serumu.",
        description="Roselle C Vitamini Serumu, cildin mat görünümünü giderir, ton eşitliği sağlar ve cilde doğal bir parlaklık kazandırır. Çevresel etkenlere karşı koruma sağlar.",
        ingredients="Vitamin C (Askorbik Asit), E Vitamini, Hyaluronik Asit, Panthenol.",
        usage_info="Günde bir kez, tercihen akşamları temiz cilde uygulayınız. Gündüz kullanımda mutlaka güneş koruyucu sürünüz.",
        volume="30 ML / 1.01 fl.oz.",
        image="products/vitamin_c.jpeg",
        image_hover="products/vitamin_c_hover.jpeg",
        price=399.90,
        badge="yeni",
        dominant_color="#B8956A",
        is_featured=True,
        order=5
    )
    ProductImage.objects.create(product=vitamin_c, image="products/gallery/vitamin_c_ad.jpeg", alt_text="C Vitamini Detayları", order=1)

    # Product 6
    kolajen = Product.objects.create(
        category=cilt_bakim,
        name="Sıkılaştırıcı Kolajen Serum",
        short_description="Cildin elastikiyetini artıran, nem depo edici yoğun kolajen bakımı.",
        description="Yaşlanma belirtilerine karşı cildi dolgunlaştıran ve nem dengesini koruyan özel kolajen serumudur. Cildin daha taze ve pürüzsüz görünmesini destekler.",
        ingredients="Hidrolize Kolajen, Hyaluronik Asit, Aloe Vera Yaprak Suyu.",
        volume="30 ML / 1.01 fl.oz.",
        image="products/kolajen_serum.jpeg",
        price=419.90,
        badge="",
        dominant_color="#7A9E7E",
        is_featured=True,
        order=6
    )

    # Product 7
    retinol = Product.objects.create(
        category=cilt_bakim,
        name="Yenileyici Retinol Serum",
        short_description="Hücre yenilenmesini hızlandıran, kırışıklık ve leke karşıtı gece serumu.",
        description="Gece bakım rutini için geliştirilen Retinol Serum, cildin kolajen üretimini destekleyerek kırışıklıkların açılmasını sağlar ve gözenek görünümünü azaltır.",
        ingredients="Retinol (%0.5), Squalane, E Vitamini, Jojoba Yağı.",
        volume="30 ML / 1.01 fl.oz.",
        image="products/retinol_serum.jpeg",
        price=479.90,
        badge="ozel",
        dominant_color="#B8857A",
        is_featured=True,
        order=7
    )

    # Product 8
    peeling = Product.objects.create(
        category=cilt_bakim,
        name="AHA %15 + BHA %2 Kırmızı Peeling Serum",
        short_description="Ölü hücreleri temizleyen, gözenek sıkılaştırıcı ve arındırıcı cilt peeling serumu.",
        description="Cildin üst tabakasındaki ölü hücreleri nazikçe soyarak taze ve aydınlık bir cilt ortaya çıkarır. Gözeneklerin temizlenmesini sağlayarak siyah nokta oluşumunu önler.",
        ingredients="AHA (Glikolik Asit, Laktik Asit), BHA (Salisilik Asit), Tazmanya Biberi Ekstratı (irite önleyici), Hyaluronik Asit.",
        usage_info="Göz çevresi hariç temiz ve kuru cilde uygulayın. En fazla 10 dakika bekletip bol suyla durulayın. Haftada en fazla 2 kez kullanılması önerilir.",
        volume="30 ML / 1.01 fl.oz.",
        image="products/peeling_serum.jpeg",
        image_hover="products/peeling_serum_hover.jpeg",
        price=369.90,
        badge="cok-satan",
        dominant_color="#C4707E",
        is_featured=True,
        order=8
    )
    ProductImage.objects.create(product=peeling, image="products/gallery/peeling_serum_ad.jpeg", alt_text="Peeling Serum Kullanımı", order=1)

    print("Products seeded successfully.")

    # 7. Services
    Service.objects.all().delete()
    Service.objects.create(
        name="Profesyonel Cilt Analizi",
        slug="profesyonel-cilt-analizi",
        short_description="Cildinizin ihtiyaçlarını modern cihazlarla analiz edip size özel bakım programı oluşturuyoruz.",
        description="Cilt tipi tespiti, nem oranı, gözenek yapısı ve leke analizi gibi detaylı testlerle cildinizin tüm özelliklerini raporluyoruz.",
        image="gallery/29.jpeg",
        icon="fas fa-magic",
        order=1
    )
    Service.objects.create(
        name="Saç & Saç Derisi Analizi",
        slug="sac-ve-sac-derisi-analizi",
        short_description="Saç dökülmesi ve yıpranma problemlerinin kökenini belirlemek için saç derinizi inceliyoruz.",
        description="Kamera destekli analizlerle saç köklerinizin sağlığını ve saç derisi gözeneklerini kontrol edip en doğru serum rutininizi belirliyoruz.",
        image="gallery/2.jpeg",
        icon="fas fa-hand-holding-heart",
        order=2
    )
    print("Services seeded.")

    # 8. About Section
    AboutSection.objects.all().delete()
    AboutSection.objects.create(
        title="Güzelliğinize Değer Katıyoruz",
        subtitle="Roselle Beauty & Care Hakkında",
        content="Doğanın en saf özlerini modern kozmetik bilimiyle buluşturarak, saç ve cilt sağlığınız için en güvenli, temiz ve etkili bakım çözümlerini sunuyoruz. Her formülümüz titiz AR-GE çalışmaları sonucu ortaya çıkmaktadır.",
        story="Kozmetik sektöründeki yılların birikimiyle kurulan Roselle Skincare, cilt ve saç sağlığında dürüstlük ve etkinlik ilkelerini benimsemiştir. Ürünlerimizde paraben, sülfat veya cilde zararlı kimyasallar kullanmıyoruz.",
        mission="Müşterilerimizin kendilerini en iyi hissetmelerini sağlayacak, doğaya saygılı ve yüksek etkili kişisel bakım formülleri sunmak.",
        vision="Türkiye ve dünyada doğal içerikli lüks kozmetik dendiğinde ilk akla gelen premium ve güvenilir marka olmak.",
        image="about/about_main.jpeg",
        years_experience=7,
        happy_customers=15000,
        products_count=8,
        natural_ingredients=98
    )
    print("About section seeded.")

    # 9. FAQs
    FAQ.objects.all().delete()
    FAQ.objects.create(
        question="Serumları hangi sırayla uygulamalıyım?",
        answer="Genel kural olarak en hafif su bazlı serumdan en yoğun yağ bazlı seruma doğru uygulama yapılmalıdır. Örneğin önce Hyaluronik asit, ardından nemlendirici veya yağ bazlı saç bakım ürünleri uygulanmalıdır.",
        order=1
    )
    FAQ.objects.create(
        question="Retinol ve C Vitamini aynı anda kullanılır mı?",
        answer="Hayır, ikisi de güçlü asit türevleri olduğundan aynı rutinde (üst üste) sürülmesi iritasyona yol açabilir. C vitaminini sabah rutininde, Retinolü ise gece rutininde kullanmanız en doğrusudur.",
        order=2
    )
    FAQ.objects.create(
        question="Ürünleriniz hamilelikte kullanılabilir mi?",
        answer="Retinol içeren ürünler hamilelik ve emzirme döneminde tavsiye edilmez. Bunun dışındaki doğal içerikli nemlendirici, kolajen ve saç serumlarımızı doktorunuza danışarak kullanabilirsiniz.",
        order=3
    )
    print("FAQs seeded.")

    # 10. Contact Info
    ContactInfo.objects.all().delete()
    ContactInfo.objects.create(
        address="Roselle Beauty Plaza, Kat: 3, Şişli / İstanbul",
        phone="+90 212 555 12 12",
        email="info@rosellebeauty.com",
        whatsapp="905551234567",
        map_embed='<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d192697.88850616608!2d28.865544258385315!3d41.00523673065095!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14caa70401680fd1%3A0x1c90a4ad6db4520!2zxLBzdGFuYnVs!5e0!3m2!1str!2str!4v1700000000000!5m2!1str!2str" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>',
        working_hours_weekday="09:00 - 19:00",
        working_hours_saturday="10:00 - 17:00",
        working_hours_sunday="Kapalı"
    )
    print("Contact info seeded.")

    # 11. Social Media
    SocialMedia.objects.all().delete()
    SocialMedia.objects.create(platform="instagram", url="https://instagram.com/rosellebeauty", order=1)
    SocialMedia.objects.create(platform="whatsapp", url="https://wa.me/905551234567", order=2)
    SocialMedia.objects.create(platform="google_business", url="https://google.com", order=3)
    print("Social media seeded.")

    # 12. Testimonials
    Testimonial.objects.all().delete()
    Testimonial.objects.create(
        name="Merve Yılmaz",
        role="Mimar",
        text="Saç dökülme serumunu 1 aydır kullanıyorum. Saçlarımda belirgin bir kalınlaşma ve bebek saçlarımda çıkma fark ettim. Kesinlikle harika bir ürün!",
        rating=5,
        order=1
    )
    Testimonial.objects.create(
        name="Elif Demir",
        role="Öğretmen",
        text="C Vitamini ve Leke Serumunu birlikte kullanıyorum. Cildimdeki güneş lekeleri gözle görülür şekilde hafifledi ve yüzüme canlılık geldi.",
        rating=5,
        order=2
    )
    Testimonial.objects.create(
        name="Selin Kaya",
        role="Diyetisyen",
        text="Retinol serumunu ilk defa denedim, cildimde herhangi bir hassasiyet yapmadı. İpeksi dokusu ve kokusu çok güzel.",
        rating=4,
        order=3
    )
    print("Testimonials seeded.")

    # 13. Blog
    BlogCategory.objects.all().delete()
    bakim_tuyo = BlogCategory.objects.create(name="Bakım Tüyoları", order=1)
    urun_inceleme = BlogCategory.objects.create(name="Ürün İncelemeleri", order=2)

    BlogPost.objects.all().delete()
    BlogPost.objects.create(
        category=bakim_tuyo,
        title="Adım Adım Gece Cilt Bakım Rutini Nasıl Olmalıdır?",
        excerpt="Gece uykusu sırasında cildimiz kendini yeniler. Peki bu süreci en verimli hale getirmek için hangi ürünleri hangi sırayla sürmeliyiz?",
        content="Cilt bakımı geceleri çok daha etkilidir çünkü hücre yenilenmesi bu saatlerde maksimuma ulaşır.\n\n1. Temizleme: İlk adım olarak cildinizi makyaj ve kirden arındırın.\n2. Tonik: Cildin pH dengesini sağlayın.\n3. Serum: Hücre yenilenmesini tetikleyen Kolajen veya Retinol serumlarımızı uygulayın.\n4. Nemlendirme: Son adım olarak nemi hapsetmek için gece kreminizi uygulayın.",
        cover_image="gallery/29.jpeg",
        read_time=4,
        is_published=True,
        is_featured=True
    )
    BlogPost.objects.create(
        category=urun_inceleme,
        title="Niasinamid (B3 Vitamini) Nedir ve Cilde Faydaları Nelerdir?",
        excerpt="Cilt bariyerini güçlendiren, lekeleri açan ve sebum dengesini sağlayan mucizevi içerik Niasinamidi mercek altına alıyoruz.",
        content="Niasinamid, son yıllarda cilt bakımının en popüler içeriklerinden biridir.\n\nFaydaları:\n- Gözeneklerin sıkılaşmasını destekler.\n- Cilt leke görünümünü azaltır.\n- Akne ve kızarıklık oluşumunu engeller.\n- Nem kaybını önleyerek bariyeri onarır.\n\nRoselle Leke Karşıtı Niacinamide Serum bu faydaları tek bir şişede sunmaktadır.",
        cover_image="gallery/15.jpeg",
        read_time=5,
        is_published=True,
        is_featured=True
    )
    print("Blog seeded.")

    # 14. Gallery Images
    GalleryImage.objects.all().delete()
    GalleryImage.objects.create(title="Saç Serumu Kadın", image="gallery/1.jpeg", order=1)
    GalleryImage.objects.create(title="Besleyici Saç Yağı", image="gallery/5.jpeg", order=2)
    GalleryImage.objects.create(title="Anti Aging Serum", image="gallery/6.jpeg", order=3)
    GalleryImage.objects.create(title="Leke Karşıtı Serum", image="gallery/15.jpeg", order=4)
    GalleryImage.objects.create(title="Peeling Serum", image="gallery/13.jpeg", order=5)
    print("Gallery images seeded.")

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
