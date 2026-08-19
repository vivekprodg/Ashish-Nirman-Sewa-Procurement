import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.contrib.staticfiles import finders

from xhtml2pdf import pisa

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access 
    letterhead graphics, static images, and fonts without broken image errors on cPanel.
    """
    # 1. Handle dynamic media files (e.g. uploaded letterheads)
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    # 2. Handle static assets (CSS, logos, backgrounds)
    elif uri.startswith(settings.STATIC_URL):
        relative_path = uri.replace(settings.STATIC_URL, "")
        path = os.path.join(settings.STATIC_ROOT, relative_path) if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT else ""
        if not os.path.isfile(path):
            found_path = finders.find(relative_path)
            path = found_path if found_path else path
    else:
        path = uri

    # 3. Fallback direct disk check
    if not os.path.isfile(path):
        candidate_media = os.path.join(settings.MEDIA_ROOT, uri.lstrip('/'))
        if os.path.isfile(candidate_media):
            return candidate_media
        return uri
    return path

def render_to_pdf(template_src, context_dict=None):
    """
    Renders an HTML template into a high-fidelity PDF stream with UTF-8 support
    and integrated letterhead resolution via link_callback.
    """
    if context_dict is None:
        context_dict = {}
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")),
        result,
        encoding='utf-8',
        link_callback=link_callback
    )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None