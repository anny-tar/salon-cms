from .models import SiteSettings, SitePage


def site_settings(request):
    site = SiteSettings.get()

    # Навигация из SitePage — только видимые, в нужном порядке
    pages = SitePage.objects.filter(is_visible=True).order_by('order')
    sections_nav = [
        {'label': p.nav_label, 'url': p.get_url()}
        for p in pages
    ]

    # Google Fonts URL
    font_url = ''
    if site.font:
        font_slug = site.font.replace(' ', '+')
        font_url = (
            f'https://fonts.googleapis.com/css2?'
            f'family={font_slug}:wght@400;500;700&display=swap'
        )

    return {
        'site_settings':   site,
        'sections_nav':    sections_nav,
        'google_font_url': font_url,
    }