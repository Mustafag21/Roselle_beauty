/**
 * Roselle Beauty & Care — Navigation JS
 * Mega menu, scroll navbar, hamburger, smooth scroll
 */
document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.getElementById('navbar');
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');
    const navOverlay = document.getElementById('navOverlay');

    // — Scroll Navbar & ScrollSpy ——————————————————————————————
    let lastScroll = 0;
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    // Mapping section IDs to their corresponding navbar link paths
    const sectionToPathMap = {
        'hero': '/',
        'products': '/urunler/',
        'services': '/hizmetler/',
        'about-preview': '/hakkimizda/',
        'blog': '/blog/',
        'contact': '/iletisim/'
    };

    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;
        
        // Navbar shrink effect
        if (currentScroll > 50) {
            navbar.classList.add('is-scrolled');
        } else {
            navbar.classList.remove('is-scrolled');
        }
        
        // ScrollSpy logic (only if on homepage where these sections exist)
        if (sections.length > 0 && window.location.pathname === '/') {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                if (currentScroll >= (sectionTop - navbar.offsetHeight - 100)) {
                    current = section.getAttribute('id');
                }
            });

            if (current && sectionToPathMap[current]) {
                const activePath = sectionToPathMap[current];
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === activePath) {
                        link.classList.add('active');
                    }
                });
            }
        }
        
        lastScroll = currentScroll;
    }, { passive: true });

    const mobileMenuDrawer = document.getElementById('mobileMenuDrawer');
    const overlay = document.getElementById('navOverlay');

    // Hamburger Menu Toggle
    if (hamburger && mobileMenuDrawer && overlay) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('is-active');
            mobileMenuDrawer.classList.toggle('is-active');
            overlay.classList.toggle('is-active');
            document.body.style.overflow = mobileMenuDrawer.classList.contains('is-active') ? 'hidden' : '';
        });

        // Close on overlay click
        overlay.addEventListener('click', closeMenu);

        // Close on link click inside mobile drawer
        mobileMenuDrawer.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMenu);
        });
    }

    function closeMenu() {
        if(hamburger) hamburger.classList.remove('is-active');
        if(mobileMenuDrawer) mobileMenuDrawer.classList.remove('is-active');
        if(overlay) overlay.classList.remove('is-active');
        document.body.style.overflow = '';
    }

    // — Smooth Scroll for anchor links ——————————————
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                const offset = navbar.offsetHeight + 20;
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

    // — Back to Top ——————————————————————————————
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                backToTop.classList.add('is-visible');
            } else {
                backToTop.classList.remove('is-visible');
            }
        }, { passive: true });
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // — Preloader ——————————————————————————————
    const preloader = document.getElementById('preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            setTimeout(() => preloader.classList.add('is-hidden'), 500);
        });
    }
});
