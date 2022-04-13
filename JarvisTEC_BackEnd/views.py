from django.http import HttpResponse
from django.template import Template, Context


def home(request):
    document = """
    <html>
        <body>
            <h1>View home</h1>
        </body>
    </html>
    """
    return HttpResponse(document)
