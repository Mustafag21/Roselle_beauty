/**
 * Roselle Beauty & Care — Animations JS
 * Scroll reveal, counter, FAQ accordion, tabs, hero slider, newsletter/contact AJAX
 */
document.addEventListener('DOMContentLoaded', () => {

    // ═════════════════════════════════════════════════════════
    // SCROLL REVEAL (Intersection Observer)
    // ═════════════════════════════════════════════════════════
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger-children');
    if (revealElements.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
        revealElements.forEach(el => observer.observe(el));
    }

    // ═════════════════════════════════════════════════════════
    // COUNTER ANIMATION
    // ═════════════════════════════════════════════════════════
    const counters = document.querySelectorAll('.counter[data-target]');
    if (counters.length) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.dataset.target);
                    const suffix = el.dataset.suffix || '';
                    const duration = 2000;
                    const start = 0;
                    const startTime = performance.now();

                    function updateCounter(currentTime) {
                        const elapsed = currentTime - startTime;
                        const progress = Math.min(elapsed / duration, 1);
                        const easeOut = 1 - Math.pow(1 - progress, 3);
                        const current = Math.round(start + (target - start) * easeOut);
                        el.textContent = current.toLocaleString('tr-TR') + suffix;
                        if (progress < 1) requestAnimationFrame(updateCounter);
                    }
                    requestAnimationFrame(updateCounter);
                    counterObserver.unobserve(el);
                }
            });
        }, { threshold: 0.3 });
        counters.forEach(el => counterObserver.observe(el));
    }

    // ═════════════════════════════════════════════════════════
    // FAQ ACCORDION
    // ═════════════════════════════════════════════════════════
    document.querySelectorAll('.faq-item__question').forEach(btn => {
        btn.addEventListener('click', () => {
            const item = btn.closest('.faq-item');
            const answer = item.querySelector('.faq-item__answer');
            const isOpen = item.classList.contains('is-open');

            // Close all
            document.querySelectorAll('.faq-item').forEach(faq => {
                faq.classList.remove('is-open');
                faq.querySelector('.faq-item__answer').style.maxHeight = '0';
            });

            // Open clicked (if was closed)
            if (!isOpen) {
                item.classList.add('is-open');
                answer.style.maxHeight = answer.scrollHeight + 'px';
            }
        });
    });

    // ═════════════════════════════════════════════════════════
    // TABS (Product Detail)
    // ═════════════════════════════════════════════════════════
    document.querySelectorAll('.tabs').forEach(tabContainer => {
        const buttons = tabContainer.querySelectorAll('.tabs__btn');
        const panels = tabContainer.querySelectorAll('.tabs__content');

        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const target = btn.dataset.tab;
                buttons.forEach(b => b.classList.remove('is-active'));
                panels.forEach(p => p.classList.remove('is-active'));
                btn.classList.add('is-active');
                tabContainer.querySelector(`#${target}`)?.classList.add('is-active');
            });
        });
    });

    // ═════════════════════════════════════════════════════════
    // HERO SLIDER
    // ═════════════════════════════════════════════════════════
    const heroSlides = document.querySelectorAll('.hero__slide');
    const heroDots = document.querySelectorAll('.hero__dot');
    if (heroSlides.length > 1) {
        let currentSlide = 0;
        const totalSlides = heroSlides.length;

        function showSlide(index) {
            heroSlides.forEach(s => s.classList.remove('is-active'));
            heroDots.forEach(d => d.classList.remove('is-active'));
            heroSlides[index].classList.add('is-active');
            heroDots[index]?.classList.add('is-active');
            currentSlide = index;
        }

        heroDots.forEach(dot => {
            dot.addEventListener('click', () => showSlide(parseInt(dot.dataset.index)));
        });

        // Auto-advance
        setInterval(() => {
            showSlide((currentSlide + 1) % totalSlides);
        }, 6000);
    }

    // ═════════════════════════════════════════════════════════
    // CONTACT FORM AJAX
    // ═════════════════════════════════════════════════════════
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gönderiliyor...';
            submitBtn.disabled = true;

            try {
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    body: new FormData(contactForm),
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await response.json();
                showToast(data.message, data.success ? 'success' : 'error');
                if (data.success) contactForm.reset();
            } catch {
                showToast('Bir hata oluştu. Lütfen tekrar deneyin.', 'error');
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }

    // ═════════════════════════════════════════════════════════
    // NEWSLETTER FORM AJAX
    // ═════════════════════════════════════════════════════════
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            try {
                const response = await fetch(newsletterForm.action, {
                    method: 'POST',
                    body: new FormData(newsletterForm),
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await response.json();
                showToast(data.message, data.success ? 'success' : 'error');
                if (data.success) newsletterForm.reset();
            } catch {
                showToast('Bir hata oluştu.', 'error');
            }
        });
    }

    // ═════════════════════════════════════════════════════════
    // TOAST NOTIFICATION
    // ═════════════════════════════════════════════════════════
    function showToast(message, type = 'success') {
        const existing = document.querySelector('.toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = `toast toast--${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        requestAnimationFrame(() => {
            toast.classList.add('is-visible');
        });

        setTimeout(() => {
            toast.classList.remove('is-visible');
            setTimeout(() => toast.remove(), 400);
        }, 4000);
    }

    // Make showToast globally available
    window.showToast = showToast;

    // ═════════════════════════════════════════════════════════
    // PRODUCT IMAGE GALLERY (Detail Page)
    // ═════════════════════════════════════════════════════════
    const mainImage = document.getElementById('productMainImage');
    const thumbs = document.querySelectorAll('.product-detail__thumb');
    if (mainImage && thumbs.length) {
        thumbs.forEach(thumb => {
            thumb.addEventListener('click', () => {
                thumbs.forEach(t => t.classList.remove('is-active'));
                thumb.classList.add('is-active');
                mainImage.src = thumb.querySelector('img').dataset.full || thumb.querySelector('img').src;
            });
        });
    }
});
