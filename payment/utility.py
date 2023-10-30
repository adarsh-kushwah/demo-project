from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.http import HttpResponse


def generate_pdf(request, template_name, context):
    html = render_to_string(template_name, context)
    pdf_file = HTML(string=html, base_url="").write_pdf()
    # response = HttpResponse(pdf_file, content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="test.pdf"'
    return pdf_file
