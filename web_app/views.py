from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import (
    Dashboard,
    DigitalSolution,
    DashboardTag,
    HelpContent,
    DasboardLog,
    ClientUser,
)

# import settings
from django.conf import settings


def logout(request):
    auth_logout(request)
    return redirect('https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri=https://testdash.ingejei.com/accounts/')

@method_decorator(login_required, name="dispatch")
class IndexView(TemplateView):
    """
    Index view.
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(settings.SITE_CONTEXT)

        if self.request.user.is_staff:
            context["digital_solutions"] = DigitalSolution.objects.all()
        else:
            try:
                context["digital_solutions"] = ClientUser.objects.get(
                    id=self.request.user.id
                ).get_digital_solutions()
            except:
                context["digital_solutions"] = None

        return context


@method_decorator(login_required, name="dispatch")
class DashboardsView(TemplateView):
    """
    Dashboards View.

    """

    template_name = "dashboards.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardsView, self).get_context_data(**kwargs)
        context.update(settings.SITE_CONTEXT)
        filter = self.request.GET.get("filter")
        digital_solution_id = kwargs.get("digital_solution_id")
        if filter == "all":
            context["dashboards"] = Dashboard.objects.filter(
                clients=self.request.user.client,
                digital_solution__id=digital_solution_id,
            ).order_by("-id")
            context["filter"] = "all"
        else:
            context["dashboards"] = Dashboard.objects.filter(
                clients=self.request.user.client,
                digital_solution__id=digital_solution_id,
                tags=filter,
            ).order_by("-id")
            context["filter"] = filter
        context["tags"] = DashboardTag.objects.filter(
            dashboard__digital_solution__id=digital_solution_id
        ).distinct()

        return context


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    """
    Dashboard view.

    """

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update(settings.SITE_CONTEXT)
        context["dashboard"] = Dashboard.objects.get(
            id=kwargs.get("dashboard_id"), clients=self.request.user.client
        )
        self.log_dashboard(kwargs.get("dashboard_id"))
        return context

    def log_dashboard(self, dashboard_id):
        """
        Log dashboard.

        """

        log = DasboardLog()
        log.dashboard = Dashboard.objects.get(id=dashboard_id)
        log.user = self.request.user
        log.device = self.request.META.get("HTTP_SEC_CH_UA")
        log.browser = self.request.META.get("HTTP_SEC_CH_UA_MOBILE")
        log.ip = self.request.META.get("REMOTE_ADDR")
        log.save()


@method_decorator(login_required, name="dispatch")
class JSView(TemplateView):
    """
    return as a js file

    """

    template_name = "js.html"

    def get_context_data(self, **kwargs):
        context = super(JSView, self).get_context_data(**kwargs)
        context.update(settings.SITE_CONTEXT)
        context["dashboard"] = Dashboard.objects.get(
            id=kwargs.get("dashboard_id"), users=self.request.user
        )
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs["content_type"] = "application/javascript"
        return super(JSView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class HelpView(TemplateView):
    """
    Help view.

    """

    template_name = "help.html"

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context.update(settings.SITE_CONTEXT)
        context["help_contents"] = HelpContent.objects.all().order_by("section__id")
        return context


class CertificateView(TemplateView):
    """
    Certificate view.

    """

    template_name = "certificate.txt"

    def get_context_data(self, **kwargs):
        context = super(CertificateView, self).get_context_data(**kwargs)
        context.update(settings.SITE_CONTEXT)
        return context