from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView

from . import utils
from .forms import UrlForm
from .models import UrlRecord

# Create your views here.
User = get_user_model()


def resolve(request, urltag):
    if len(urltag) < settings.URLTAG_MAX_LENGTH:
        # don't check database if not required
        raise Http404
    url_record = get_object_or_404(UrlRecord, pk=urltag)
    original_url = url_record.original_url
    return redirect(original_url)


class UrlRecordCreate(CreateView):
    form_class = UrlForm
    template_name = 'shortener/index.html'
    success_url = "/"

    def form_valid(self, form):
        try:
            user = User.objects.get(username=self.request.user)
        except User.DoesNotExist:
            user = None
        form.instance.user = user
        if user:
            if user.is_staff:  # one year if staff
                form.instance.date_expiry = utils.get_date_one_year_from_today()
            else:  # three months if authenticated
                form.instance.date_expiry = utils.get_date_three_months_from_today()
        else:  # one week if not authenticated
            form.instance.date_expiry = utils.get_date_one_week_from_today()

        form.instance.short_url = utils.get_random_generated_shortcode()
        return super().form_valid(form)


url_record_create = UrlRecordCreate.as_view()
