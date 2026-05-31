from .models import SiteSettings, Section

SECTION_NAV_MAP = {
    'services':  {'label': 'Услуги',          'url': '/services/'},
    'team':      {'label': 'Команда',         'url': '/team/'},
    'portfolio': {'label': 'Портфолио',       'url': '/portfolio/'},
    'news':      {'label': 'Новости и акции', 'url': '/news/'},
    'products':  {'label': 'Товары',          'url': '/products/'},
}

def site_settings(request):
    site = SiteSettings.get()
    sections = Section.objects.filter(site=site).order_by('order')
    sections_nav = []
    seen = set()
    for s in sections:
        if s.type in SECTION_NAV_MAP and s.type not in seen:
            sections_nav.append(SECTION_NAV_MAP[s.type])
            seen.add(s.type)
    return {
        'site_settings': site,
        'sections_nav': sections_nav,
    }