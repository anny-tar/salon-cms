from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import SiteSettings
from .sections import AVAILABLE_SECTIONS, get_sections_config
import json


@staff_member_required
def manage_sections(request):
    site = SiteSettings.get()
    config = get_sections_config(site)

    # Дополняем конфиг метаданными секций
    sections_map = {s['key']: s for s in AVAILABLE_SECTIONS}
    enriched = []
    for item in config:
        key = item['key']
        if key in sections_map:
            enriched.append({
                **item,
                'label': sections_map[key]['label'],
                'type': sections_map[key]['type'],
            })

    if request.method == 'POST':
        new_config = []
        keys = request.POST.getlist('keys')
        for i, key in enumerate(keys):
            enabled = request.POST.get(f'enabled_{key}') == 'on'
            new_config.append({
                'key': key,
                'enabled': enabled,
                'order': i + 1,
            })
        site.sections_config = new_config
        site.save()
        return redirect('admin:site_constructor_sitesettings_change', site.pk)

    return render(request, 'admin/site_constructor/manage_sections.html', {
        'sections': enriched,
        'title': 'Управление секциями сайта',
    })