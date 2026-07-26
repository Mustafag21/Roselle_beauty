"""
Roselle Beauty & Care — Views (Tam Yeniden Tasarım)
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import (
    HeroBanner, Product, ProductCategory, Service,
    AboutSection, ContactInfo, ContactMessage, Testimonial,
    BlogPost, BlogCategory, FAQ, GalleryImage, BrandFeature,
    Newsletter, SiteSettings,
)
from .forms import ContactForm, NewsletterForm


def home(request):
    context = {
        'banners': HeroBanner.objects.filter(is_active=True),
        'featured_products': Product.objects.filter(is_active=True, is_featured=True)[:8],
        'products': Product.objects.filter(is_active=True)[:8],
        'categories': ProductCategory.objects.filter(is_active=True),
        'services': Service.objects.filter(is_active=True)[:6],
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
        'blog_posts': BlogPost.objects.filter(is_published=True)[:3],
        'faqs': FAQ.objects.filter(is_active=True)[:6],
        'brand_features': BrandFeature.objects.filter(is_active=True),
        'about': AboutSection.get_about(),
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'index.html', context)


def products_page(request):
    category_slug = request.GET.get('kategori')
    products = Product.objects.filter(is_active=True)
    if category_slug:
        products = products.filter(category__slug=category_slug)
    context = {
        'products': products,
        'categories': ProductCategory.objects.filter(is_active=True),
        'active_category': category_slug,
    }
    return render(request, 'products.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(
        is_active=True, category=product.category
    ).exclude(pk=product.pk)[:4]
    context = {
        'product': product,
        'related_products': related,
    }
    return render(request, 'product_detail.html', context)


def services_page(request):
    context = {
        'services': Service.objects.filter(is_active=True),
    }
    return render(request, 'services.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    other_services = Service.objects.filter(is_active=True).exclude(pk=service.pk)[:4]
    context = {
        'service': service,
        'other_services': other_services,
    }
    return render(request, 'service_detail.html', context)


def about_page(request):
    context = {
        'about': AboutSection.get_about(),
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
        'gallery_images': GalleryImage.objects.filter(is_active=True)[:12],
    }
    return render(request, 'about.html', context)


def contact_page(request):
    context = {
        'form': ContactForm(),
        'contact': ContactInfo.get_contact(),
    }
    return render(request, 'contact.html', context)


@require_POST
def contact_submit(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Mesajınız başarıyla gönderildi!'})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def blog_page(request):
    category_slug = request.GET.get('kategori')
    posts = BlogPost.objects.filter(is_published=True)
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    context = {
        'posts': posts,
        'categories': BlogCategory.objects.all(),
        'active_category': category_slug,
    }
    return render(request, 'blog.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(pk=post.pk)[:3]
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog_detail.html', context)


def faq_page(request):
    context = {
        'faqs': FAQ.objects.filter(is_active=True),
    }
    return render(request, 'faq.html', context)


@require_POST
def newsletter_subscribe(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        obj, created = Newsletter.objects.get_or_create(email=email)
        if created:
            return JsonResponse({'success': True, 'message': 'Bültenimize başarıyla abone oldunuz!'})
        else:
            return JsonResponse({'success': True, 'message': 'Bu e-posta zaten kayıtlı.'})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def search_page(request):
    query = request.GET.get('q', '')
    products = []
    blog_posts = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) |
            Q(short_description__icontains=query),
            is_active=True
        )
        blog_posts = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            is_published=True
        )
    context = {
        'query': query,
        'products': products,
        'blog_posts': blog_posts,
    }
    return render(request, 'search.html', context)
