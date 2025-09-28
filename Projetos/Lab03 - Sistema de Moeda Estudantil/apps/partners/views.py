from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

@method_decorator(login_required, name="dispatch")
class EmpresaCreateView(TemplateView):
    template_name = "partners/empresa_create.html"

@method_decorator(login_required, name="dispatch")
class ResgatesListView(TemplateView):
    template_name = "partners/resgates_list.html"
