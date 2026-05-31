from .models import SiteSettings, Section

SECTION_NAV_MAP = {
    'services':  {'label': 'Услуги',          'url': '/services/',  'flag': 'show_services'},
    'team':      {'label': 'Команда',         'url': '/team/',      'flag': 'show_team'},
    'portfolio': {'label': 'Портфолио',       'url': '/portfolio/', 'flag': 'show_portfolio'},
    'news':      {'label': 'Новости и акции', 'url': '/news/',      'flag': 'show_news'},
    'products':  {'label': 'Товары',          'url': '/products/',  'flag': 'show_products'},
}

def site_settings(request):
    site = SiteSettings.get()
    sections_nav = []
    for key, data in SECTION_NAV_MAP.items():
        if getattr(site, data['flag'], False):
            sections_nav.append({'label': data['label'], 'url': data['url']})
    return {
        'site_settings': site,
        'sections_nav': sections_nav,
    }