from django.shortcuts import render
from django.views import View 

from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import HttpResponse
# Create your views here.
from django.template.loader import render_to_string

class GenerateBillView(View):

    def pdf_generation(self, request):
        html = render_to_string('test1.html', {'name':'Adarsh'})
        pdf_file = HTML(string=html,base_url="").write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="test.pdf"'
        return response

    def get(self, request, *args, **kwargs):
        context = {}  # Add something to your context object here
        p = self.pdf_generation(request)
        return p


