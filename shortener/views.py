from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from . import utils
from .forms import UrlForm
from .models import UrlRecord
from django.utils import timezone

# Create your views here.
User = get_user_model()


def resolve(request, urltag):
    if len(urltag) < settings.URLTAG_MAX_LENGTH:
        # don't check database if not required
        raise Http404
    url_record = get_object_or_404(UrlRecord, pk=urltag)
    if url_record.is_expired:
        raise Http404
    original_url = url_record.original_url
    return redirect(original_url)


def detail(request, urltag):
    if len(urltag) < settings.URLTAG_MAX_LENGTH:
        # don't check database if not required
        raise Http404
    url_record = get_object_or_404(UrlRecord, pk=urltag)
    if url_record.is_expired:
        raise Http404
    urltag = url_record.short_url
    context = {
        "url_record": url_record,
        "urltag": urltag
    }
    return render(request, "shortener/detail.html", context)


class UrlRecordCreate(CreateView):
    form_class = UrlForm
    template_name = 'shortener/index.html'

    def get_success_url(self):
        return reverse_lazy(
            'url_detail',
            kwargs={"urltag": self.object.short_url}
        )

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


class UrlsByUserListView(LoginRequiredMixin, ListView):
    template_name = "shortener/list.html"

    def get_queryset(self):
        return UrlRecord.objects.filter(user=self.request.user)


urls_by_user_list_view = UrlsByUserListView.as_view()


class ExpiredUrlsByUserListView(LoginRequiredMixin, ListView):
    template_name = "shortener/list.html"

    def get_queryset(self):
        return UrlRecord.objects.filter(
            user=self.request.user
        ).filter(
            date_expiry__lt=timezone.now().date()
        )

expired_urls_by_user_list_view = ExpiredUrlsByUserListView.as_view()
