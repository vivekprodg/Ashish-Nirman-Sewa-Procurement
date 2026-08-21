import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.contrib.staticfiles import finders

from xhtml2pdf import pisa

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system disk paths so xhtml2pdf can access
    uploaded letterheads, static logos, and fonts without broken image errors.
    """
    # 1. Direct check if path is already an existing absolute system path
    if os.path.isabs(uri) and os.path.isfile(uri):
        return uri

    path = None

    # 2. Handle Media Files (Uploaded letterhead graphics, banners, stamps)
    if uri.startswith(settings.MEDIA_URL):
        relative_path = uri[len(settings.MEDIA_URL):].lstrip('/')
        path = os.path.join(settings.MEDIA_ROOT, relative_path)
    elif '/media/' in uri:
        relative_path = uri.split('/media/', 1)[1].lstrip('/')
        path = os.path.join(settings.MEDIA_ROOT, relative_path)

    # 3. Handle Static Assets (CSS, Static Icons, Logos)
    elif uri.startswith(settings.STATIC_URL):
        relative_path = uri[len(settings.STATIC_URL):].lstrip('/')
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            static_file = os.path.join(settings.STATIC_ROOT, relative_path)
            if os.path.isfile(static_file):
                path = static_file
        if not path or not os.path.isfile(path):
            found_path = finders.find(relative_path)
            if found_path:
                path = found_path
    elif '/static/' in uri:
        relative_path = uri.split('/static/', 1)[1].lstrip('/')
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            static_file = os.path.join(settings.STATIC_ROOT, relative_path)
            if os.path.isfile(static_file):
                path = static_file
        if not path or not os.path.isfile(path):
            found_path = finders.find(relative_path)
            if found_path:
                path = found_path

    # 4. Fallback checking inside MEDIA_ROOT and STATIC_ROOT directly
    if not path or not os.path.isfile(path):
        clean_uri = uri.lstrip('/').replace('\\', '/')
        candidate_media = os.path.join(settings.MEDIA_ROOT, clean_uri)
        if os.path.isfile(candidate_media):
            return candidate_media

        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            candidate_static = os.path.join(settings.STATIC_ROOT, clean_uri)
            if os.path.isfile(candidate_static):
                return candidate_static

        # Fallback to original URI if unable to resolve
        return uri

    return path

def render_to_pdf(template_src, context_dict=None):
    """
    Renders a Django HTML template into a high-fidelity PDF stream with UTF-8 support
    and integrated letterhead link resolution via link_callback.
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