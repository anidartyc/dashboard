from django.urls import path
from web_app.views import IndexView, DashboardView, JSView, DashboardsView, HelpView , CertificateView
from . import views  # Asegúrate de que el módulo views está importado

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('dashboards/<int:digital_solution_id>/', DashboardsView.as_view(), {'filter': 'all'}, name='dashboards'),
    path('dashboard<int:dashboard_id>.js', JSView.as_view(), name='js'),
    path('dashboard/<int:dashboard_id>/', DashboardView.as_view(), name='dashboard'),
    path('help/', HelpView.as_view(), name='help'),
    path('.well-known/pki-validation/4021828EC73D9E2D1A1768FE4D6AD88A.txt', CertificateView.as_view(), name='certificate'),
    path('accounts/logout/', views.logout, name='logout'),
]