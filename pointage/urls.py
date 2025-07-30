from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'pointage'

urlpatterns = [
    path('accounts/login/', views.custom_login, name='custom_login'),
    path('', views.accueil, name='accueil'),
    path('import/', views.import_excel, name='import_excel'),
    path('excels/', views.list_excels, name='list_excels'),
    path('excels/<int:file_id>/delete/', views.delete_excel, name='delete_excel'),
    path('heures-supplementaires/', views.heures_supplementaires, name='heures_supplementaires'),
    path('heures-supplementaires/<path:filename>/', views.heures_supplementaires_file, name='heures_supplementaires_file'),
    path('statistique/', views.statistique, name='statistique'),
    
    # Manager management URLs
    path('managers/', views.manager_list, name='manager_list'),
    path('managers/add/', views.manager_create, name='manager_create'),
    path('managers/<int:pk>/edit/', views.manager_edit, name='manager_edit'),
    path('managers/<int:pk>/toggle-active/', views.manager_toggle_active, name='manager_toggle_active'),
    path('managers/<int:pk>/delete/', views.manager_delete, name='manager_delete'),
    path('settings/', login_required(views.settings), name='settings'),
    # path('managers/<int:pk>/reset-password/', views.manager_reset_password, name='manager_reset_password'),
    path('display/<path:filename>/', views.display_excel, name='display_excel'),
    path('api/person-hours/', views.get_person_hours_data, name='person_hours_data'),
    path('api/pie-chart/', views.pie_chart_data, name='pie_chart_data'),
]