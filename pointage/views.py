from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
import glob
import json
from datetime import datetime, timedelta
import math
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .models import UploadedExcel, ManagerProfile
from .forms import ManagerCreationForm, ManagerEditForm, UserSettingsForm
from urllib.parse import unquote
from django.http import HttpResponseForbidden
import calendar
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from .validators import validate_excel_file, sanitize_filename
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

MONTH_NAMES_FR = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
    7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
}

@csrf_exempt
def custom_login(request):
    """Custom login view that bypasses CSRF protection"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pointage:accueil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'registration/login.html')

@csrf_exempt
def custom_logout(request):
    """Custom logout view that bypasses CSRF protection"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('pointage:accueil')

@login_required
def import_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        try:
            # Validate the uploaded file
            validate_excel_file(excel_file)
            
            # Sanitize filename
            sanitized_filename = sanitize_filename(excel_file.name)
            excel_file.name = sanitized_filename
            
            # Save file to UploadedExcel model
            uploaded = UploadedExcel.objects.create(
                file=excel_file,
                uploaded_by=request.user
            )
            messages.success(request, f'File "{sanitized_filename}" uploaded successfully.')
            return redirect('pointage:display_excel', filename=uploaded.file.name.split('/')[-1])
            
        except ValidationError as e:
            messages.error(request, f'Upload failed: {str(e)}')
        except Exception as e:
            messages.error(request, f'An error occurred during upload: {str(e)}')
            
    return render(request, 'pointage/import_excel.html')

def display_excel(request, filename):
    file_path = os.path.join(UPLOAD_DIR, filename)
    df = pd.read_excel(file_path)
    colonnes_voulues = ["date", "name", "in", "out"]
    mapping = {col.lower(): col for col in df.columns}
    colonnes_presentes = [mapping[c] for c in colonnes_voulues if c in mapping]
    colonnes_lues = list(df.columns)
    filter_col = request.GET.get('filter_col', '')
    search = request.GET.get('search', '')

    # Filtrage par colonne (sur la vraie casse)
    if filter_col and filter_col in df.columns and search:
        df = df[df[filter_col].astype(str).str.contains(search, case=False, na=False)]

    # Affichage seulement des colonnes voulues si elles existent
    if colonnes_presentes:
        df = df[[col for col in colonnes_presentes if col in df.columns]]
        message = ''
    else:
        message = "Aucune des colonnes 'date', 'name', 'in', 'out' n'a été trouvée dans le fichier importé.\nColonnes trouvées : " + ", ".join(colonnes_lues)
        return render(request, 'pointage/display_excel.html', {'data': '', 'filename': filename, 'message': message, 'colonnes_lues': colonnes_lues, 'filter_col': filter_col, 'search': search})

    data = df.to_html(classes=['table', 'table-striped', 'custom-table'], index=False)
    return render(request, 'pointage/display_excel.html', {
        'data': data,
        'filename': filename,
        'message': message,
        'colonnes_lues': colonnes_lues,
        'filter_col': filter_col,
        'search': search,
    })

@login_required
def list_excels(request):
    user = request.user
    if user.groups.filter(name='Admin').exists() or user.is_superuser:
        files = UploadedExcel.objects.all()
    else:
        files = UploadedExcel.objects.filter(uploaded_by=user)
    return render(request, 'pointage/list_excels.html', {'files': files})

@login_required
def delete_excel(request, file_id):
    file = get_object_or_404(UploadedExcel, id=file_id)
    # Only allow the uploader or admin to delete
    if request.user != file.uploaded_by and not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer ce fichier.")
    if request.method == 'POST':
        file.file.delete(save=False)  # Delete the file from storage
        file.delete()  # Delete the DB record
        messages.success(request, "Fichier supprimé avec succès.")
    return redirect('pointage:list_excels')

def accueil(request):
    # If user is not authenticated, redirect to login page
    if not request.user.is_authenticated:
        from django.urls import reverse
        from django.shortcuts import redirect
        return redirect(reverse('login') + '?next=' + request.path)
    return render(request, 'pointage/accueil.html')

@login_required
@permission_required('pointage.can_manage_managers', raise_exception=True)
def manager_list(request):
    query = request.GET.get('q', '')
    managers = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query)
    ).order_by('-date_joined')
    
    context = {
        'managers': managers,
        'query': query
    }
    return render(request, 'pointage/manager_list.html', context)

@login_required
@permission_required('pointage.can_manage_managers', raise_exception=True)
def manager_create(request):
    if request.method == 'POST':
        form = ManagerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Manager {user.username} created successfully.')
            return redirect('pointage:manager_list')
    else:
        form = ManagerCreationForm()
    
    return render(request, 'pointage/manager_form.html', {
        'form': form,
        'title': 'Add New Manager'
    })

@login_required
@permission_required('pointage.can_manage_managers', raise_exception=True)
def manager_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ManagerEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Manager {user.username} updated successfully.')
            return redirect('pointage:manager_list')
    else:
        form = ManagerEditForm(instance=user)
    
    return render(request, 'pointage/manager_form.html', {
        'form': form,
        'title': f'Edit Manager: {user.username}'
    })

@login_required
@permission_required('pointage.can_manage_managers', raise_exception=True)
def manager_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    if hasattr(user, 'managerprofile'):
        user.managerprofile.is_active = not user.managerprofile.is_active
        user.managerprofile.save()
        status = 'activated' if user.managerprofile.is_active else 'deactivated'
        messages.success(request, f'Manager {user.username} has been {status}.')
    return redirect('pointage:manager_list')

@login_required
@permission_required('pointage.can_manage_managers', raise_exception=True)
def manager_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Manager {username} has been deleted.')
        return redirect('pointage:manager_list')
    return render(request, 'pointage/manager_confirm_delete.html', {'manager': user})

@login_required
def heures_supplementaires(request):
    user = request.user
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        excel_files = UploadedExcel.objects.all()
    else:
        excel_files = UploadedExcel.objects.filter(uploaded_by=user)

    resultats = []
    for uploaded_file in excel_files:
        try:
            df = pd.read_excel(uploaded_file.file.path)
            mapping = {col.lower().strip(): col for col in df.columns}

            name_col = mapping.get('name')
            in_col = mapping.get('in')
            out_col = mapping.get('out')
            date_col = mapping.get('date')
            dept_col = mapping.get('département') or mapping.get('department')
            
            if not all([name_col, in_col, out_col, date_col]):
                continue

            for _, row in df.iterrows():
                try:
                    heure_in = str(row[in_col]).strip()
                    heure_out = str(row[out_col]).strip()
                    if not heure_in or not heure_out or heure_in.lower() == 'nan' or heure_out.lower() == 'nan':
                        continue
                    t_in = datetime.strptime(heure_in, '%H:%M') if len(heure_in) <= 5 else datetime.strptime(heure_in, '%H:%M:%S')
                    t_out = datetime.strptime(heure_out, '%H:%M') if len(heure_out) <= 5 else datetime.strptime(heure_out, '%H:%M:%S')
                    duree = (t_out - t_in)
                    if duree < timedelta(0):
                        duree += timedelta(days=1)
                    heures_travaillees = duree.total_seconds() / 3600
                    heures_travaillees_arr = math.ceil(heures_travaillees)
                    # Déterminer le jour de la semaine
                    date_val = row[date_col]
                    date_obj = None
                    if isinstance(date_val, datetime):
                        date_obj = date_val
                    else:
                        date_str = str(date_val)
                        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%m/%d/%Y"):
                            try:
                                date_obj = datetime.strptime(date_str, fmt)
                                break
                            except Exception:
                                continue
                        if not date_obj:
                            continue  # Si aucun format ne marche, ignorer la ligne
                    if date_obj.weekday() in [5, 6]:  # 5=Samedi, 6=Dimanche
                        heures_sup = heures_travaillees_arr
                    else:
                        heures_sup = max(0, heures_travaillees_arr - 8)
                    if heures_sup > 0:
                        employee_name_raw = str(row[name_col]).strip()
                        department = str(row[dept_col]) if dept_col and pd.notna(row[dept_col]) else None
                        resultats.append({
                            'nom': employee_name_raw,
                            'department': department,
                            'date': row[date_col],
                            'date_obj': date_obj, # Add datetime object for filtering
                            'in': heure_in,
                            'out': heure_out,
                            'heures_sup': heures_sup,
                            'weekend': date_obj.weekday() in [5, 6],
                        })
                except Exception:
                    continue
        except Exception:
            continue
    
    all_names = sorted(list(set(str(r['nom']) for r in resultats)))
    all_departments = sorted(list(set(r['department'] for r in resultats if r.get('department'))))
    available_dates = {r['date_obj'] for r in resultats if r.get('date_obj')}
    unique_year_months = sorted(list(set((d.year, d.month) for d in available_dates)), reverse=True)
    available_months = [(f"{year}-{month}", f"{MONTH_NAMES_FR[month]} {year}") for year, month in unique_year_months]

    filter_nom = request.GET.get('filter_nom', '').strip()
    filter_month_year = request.GET.get('filter_month_year', '').strip()
    filter_department = request.GET.get('filter_department', '').strip()

    if filter_nom:
        resultats = [r for r in resultats if str(r['nom']) == filter_nom]
    if filter_department:
        resultats = [r for r in resultats if r.get('department') == filter_department]
    if filter_month_year:
        try:
            year, month = map(int, filter_month_year.split('-'))
            resultats = [r for r in resultats if r.get('date_obj') and r['date_obj'].year == year and r['date_obj'].month == month]
        except ValueError:
            pass

    total_heures_sup = sum(r['heures_sup'] for r in resultats)
    return render(request, 'pointage/heures_supplementaires.html', {
        'resultats': resultats,
        'filter_nom': filter_nom,
        'filter_month_year': filter_month_year,
        'filter_department': filter_department,
        'total_heures_sup': total_heures_sup,
        'all_names': all_names,
        'available_months': available_months,
        'all_departments': all_departments
    })

@login_required
def heures_supplementaires_file(request, filename):
    file_path = os.path.join(UPLOAD_DIR, unquote(filename))
    resultats = []
    try:
        df = pd.read_excel(file_path)
        mapping = {col.lower().strip(): col for col in df.columns}

        name_col = mapping.get('name')
        in_col = mapping.get('in')
        out_col = mapping.get('out')
        date_col = mapping.get('date')
        dept_col = mapping.get('département') or mapping.get('department')
        
        if not all([name_col, in_col, out_col, date_col]):
            return render(request, 'pointage/heures_supplementaires.html', {'resultats': [], 'error': 'Colonnes requises manquantes.'})

        for _, row in df.iterrows():
            try:
                heure_in = str(row[in_col]).strip()
                heure_out = str(row[out_col]).strip()
                if not heure_in or not heure_out or heure_in.lower() == 'nan' or heure_out.lower() == 'nan':
                    continue
                t_in = datetime.strptime(heure_in, '%H:%M') if len(heure_in) <= 5 else datetime.strptime(heure_in, '%H:%M:%S')
                t_out = datetime.strptime(heure_out, '%H:%M') if len(heure_out) <= 5 else datetime.strptime(heure_out, '%H:%M:%S')
                duree = (t_out - t_in)
                if duree < timedelta(0):
                    duree += timedelta(days=1)
                heures_travaillees = duree.total_seconds() / 3600
                heures_travaillees_arr = math.ceil(heures_travaillees)
                date_val = row[date_col]
                date_obj = None
                if isinstance(date_val, datetime):
                    date_obj = date_val
                else:
                    date_str = str(date_val)
                    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%m/%d/%Y"):
                        try:
                            date_obj = datetime.strptime(date_str, fmt)
                            break
                        except Exception:
                            continue
                    if not date_obj:
                        continue
                if date_obj.weekday() in [5, 6]:
                    heures_sup = heures_travaillees_arr
                else:
                    heures_sup = max(0, heures_travaillees_arr - 8)
                if heures_sup > 0:
                    employee_name_raw = str(row[name_col]).strip()
                    department = str(row[dept_col]) if dept_col and pd.notna(row[dept_col]) else None
                    resultats.append({
                        'nom': employee_name_raw,
                        'department': department,
                        'date': row[date_col],
                        'date_obj': date_obj,
                        'in': heure_in,
                        'out': heure_out,
                        'heures_sup': heures_sup,
                        'weekend': date_obj.weekday() in [5, 6],
                    })
            except Exception:
                continue
    except Exception:
        pass
        
    all_names = sorted(list(set(str(r['nom']) for r in resultats)))
    all_departments = sorted(list(set(r['department'] for r in resultats if r.get('department'))))
    available_dates = {r['date_obj'] for r in resultats if r.get('date_obj')}
    unique_year_months = sorted(list(set((d.year, d.month) for d in available_dates)), reverse=True)
    available_months = [(f"{year}-{month}", f"{MONTH_NAMES_FR[month]} {year}") for year, month in unique_year_months]
    
    total_heures_sup_all = sum(r['heures_sup'] for r in resultats)
    
    filter_nom = request.GET.get('filter_nom', '').strip()
    filter_month_year = request.GET.get('filter_month_year', '').strip()
    filter_department = request.GET.get('filter_department', '').strip()
    
    filtered_resultats = resultats
    
    if filter_nom:
        filtered_resultats = [r for r in filtered_resultats if str(r['nom']) == filter_nom]
    if filter_department:
        filtered_resultats = [r for r in filtered_resultats if r.get('department') == filter_department]
    if filter_month_year:
        try:
            year, month = map(int, filter_month_year.split('-'))
            filtered_resultats = [r for r in filtered_resultats if r.get('date_obj') and r['date_obj'].year == year and r['date_obj'].month == month]
        except ValueError:
            pass

    total_heures_sup_filtered = sum(r['heures_sup'] for r in filtered_resultats)
    
    return render(request, 'pointage/heures_supplementaires.html', {
        'resultats': filtered_resultats,
        'total_heures_sup': total_heures_sup_filtered,
        'total_heures_sup_all': total_heures_sup_all,
        'filename': filename,
        'filter_nom': filter_nom,
        'filter_month_year': filter_month_year,
        'filter_department': filter_department,
        'all_names': all_names,
        'available_months': available_months,
        'all_departments': all_departments
    })

from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
def settings(request):
    user = request.user
    is_admin_user = is_admin(user)
    form = None
    password_form = None
    
    if request.method == 'POST':
        if 'update_profile' in request.POST and is_admin_user:
            form = UserSettingsForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Vos paramètres ont été mis à jour avec succès !')
                return redirect('pointage:settings')
            password_form = PasswordChangeForm(user=user)
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)  # Important pour maintenir la session
                messages.success(request, 'Votre mot de passe a été modifié avec succès !')
                return redirect('pointage:settings')
    
    # Initialisation des formulaires si pas déjà fait
    if form is None and is_admin_user:
        form = UserSettingsForm(instance=user)
    if password_form is None:
        password_form = PasswordChangeForm(user=user)
    
    context = {
        'form': form,
        'password_form': password_form,
        'is_admin': is_admin_user,
    }
    return render(request, 'pointage/settings.html', context)

@login_required
def get_person_hours_data(request):
    """
    API endpoint to get hours data for a specific person or department
    
    Query Parameters:
    - person: Filter by person name
    - department: Filter by department name
    - month: Filter by month in YYYY-MM format
    """
    from django.http import JsonResponse
    from .models import UploadedExcel
    from collections import defaultdict
    
    user = request.user
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        files = UploadedExcel.objects.all()
    else:
        files = UploadedExcel.objects.filter(uploaded_by=user)

    person_name = request.GET.get('person')
    department_filter = request.GET.get('department')
    month_filter = request.GET.get('month')
    
    # Remove the restriction: if neither is present, return all data
    # Parse month filter if provided (format: YYYY-MM)
    filter_year = None
    filter_month = None
    if month_filter:
        try:
            filter_year, filter_month = map(int, month_filter.split('-'))
        except (ValueError, AttributeError):
            return JsonResponse({'error': 'Invalid month format. Use YYYY-MM'}, status=400)
    
    # Get all records matching the criteria
    records = []
    for uploaded_file in files:
        try:
            df = pd.read_excel(uploaded_file.file.path)
            mapping = {col.lower().strip(): col for col in df.columns}
            
            # Check if required columns exist
            required_cols = ['date', 'in', 'out']
            if not all(col in mapping for col in required_cols):
                continue
                
            # Filter for the specific person if specified
            if person_name:
                name_col = mapping.get('name')
                if not name_col:
                    continue
                df = df[df[name_col].astype(str).str.strip().str.lower() == person_name.lower()]
            
            # Filter by department if specified
            if department_filter:
                dept_col = mapping.get('département') or mapping.get('department')
                if not dept_col:
                    continue
                df = df[df[dept_col].astype(str).str.strip().str.lower() == department_filter.lower()]
            
            # Process each record
            for _, row in df.iterrows():
                try:
                    date_val = row[mapping['date']]
                    
                    # Skip if date is not a valid datetime
                    if not isinstance(date_val, (datetime, pd.Timestamp)) or pd.isna(date_val):
                        continue
                    
                    # Filter by month if specified
                    if filter_year is not None and filter_month is not None:
                        if date_val.year != filter_year or date_val.month != filter_month:
                            continue
                    
                    heure_in = str(row[mapping['in']]).strip()
                    heure_out = str(row[mapping['out']]).strip()
                    
                    if not all([heure_in, heure_out, heure_in.lower() != 'nan', heure_out.lower() != 'nan']):
                        continue
                        
                    t_in = datetime.strptime(heure_in, '%H:%M') if len(heure_in) <= 5 else datetime.strptime(heure_in, '%H:%M:%S')
                    t_out = datetime.strptime(heure_out, '%H:%M') if len(heure_out) <= 5 else datetime.strptime(heure_out, '%H:%M:%S')
                    
                    duree = (t_out - t_in)
                    if duree < timedelta(0):
                        duree += timedelta(days=1)
                    
                    # Calculate overtime hours
                    heures_travaillees = duree.total_seconds() / 3600
                    heures_travaillees_arr = math.ceil(heures_travaillees)
                    
                    # Check if it's a weekend (5=Saturday, 6=Sunday)
                    if date_val.weekday() in [5, 6]:
                        heures_sup = heures_travaillees_arr
                    else:
                        heures_sup = max(0, heures_travaillees_arr - 8)
                    
                    # Only include days with overtime
                    if heures_sup > 0:
                        # Get the person's name if available
                        name = row.get(mapping.get('name', ''), '')
                        records.append({
                            'date': date_val,
                            'hours': heures_sup,  # Use overtime hours instead of total hours
                            'name': str(name) if not pd.isna(name) else ''
                        })
                    
                except (ValueError, KeyError) as e:
                    continue
                    
        except Exception as e:
            continue
    
    # If a specific person is filtered, return overtime per day (current behavior)
    if person_name:
        date_hours = defaultdict(float)
        for record in records:
            date_str = record['date'].strftime('%Y-%m-%d')
            date_hours[date_str] += record['hours']
        sorted_dates = sorted(date_hours.items())
        response_data = {
            'dates': [item[0] for item in sorted_dates],
                'hours': [round(item[1], 2) for item in sorted_dates],
        }
        # Add name information if available
        if records:
            response_data['names'] = [person_name] * len(sorted_dates)
        return JsonResponse(response_data)
    
    # Otherwise, aggregate by employee name (for department/month filter or no filter)
    name_hours = defaultdict(float)
    for record in records:
        name = record.get('name', '').strip()
        if name:
            name_hours[name] += record['hours']
    sorted_names = sorted(name_hours.items(), key=lambda x: x[1], reverse=True)
    response_data = {
        'names': [item[0] for item in sorted_names],
        'hours': [round(item[1], 2) for item in sorted_names],
    }
    return JsonResponse(response_data)

def get_available_months():
    """Generate a list of available months from the database"""
    from .models import UploadedExcel
    import pandas as pd
    from datetime import datetime
    
    months = set()
    print("\n=== Starting get_available_months() ===")
    
    # Check if there are any files
    all_files = list(UploadedExcel.objects.all())
    print(f"Found {len(all_files)} Excel files to process")
    
    for uploaded_file in all_files:
        try:
            print(f"\nProcessing file: {uploaded_file.file.name}")
            print(f"File path: {uploaded_file.file.path}")
            
            # Check if file exists
            import os
            if not os.path.exists(uploaded_file.file.path):
                print(f"File does not exist: {uploaded_file.file.path}")
                continue
                
            # Read the Excel file
            try:
                df = pd.read_excel(uploaded_file.file.path)
                print(f"Successfully read Excel file")
                print(f"Columns in file: {df.columns.tolist()}")
                print(f"First few rows of data:\n{df.head()}")
            except Exception as e:
                print(f"Error reading Excel file: {e}")
                continue
            
            # Create mapping of lowercase column names to original names
            mapping = {str(col).lower().strip(): str(col) for col in df.columns}
            print(f"Column mapping: {mapping}")
            
            # Check for possible date columns (case insensitive)
            possible_date_cols = [col for col in mapping.keys() if 'date' in col.lower()]
            print(f"Possible date columns: {possible_date_cols}")
            
            for date_col in (possible_date_cols or [None]):
                date_col_name = mapping.get(date_col) if date_col else None
                print(f"\nTrying date column: {date_col_name}")
                
                if date_col_name is not None and date_col_name in df.columns:
                    print(f"Processing dates from column: {date_col_name}")
                    
                    # Make a copy to avoid SettingWithCopyWarning
                    temp_df = df[[date_col_name]].copy()
                    
                    # Convert to datetime and drop NaT values
                    temp_df['date'] = pd.to_datetime(temp_df[date_col_name], errors='coerce')
                    temp_df = temp_df.dropna(subset=['date'])
                    
                    print(f"Found {len(temp_df)} valid dates in column")
                    if not temp_df.empty:
                        print(f"Date range: {temp_df['date'].min()} to {temp_df['date'].max()}")
                    
                    # Extract unique year-month combinations
                    for date_val in temp_df['date']:
                        try:
                            if pd.notna(date_val):
                                # Format as YYYY-MM and Month YYYY (in French)
                                month_key = date_val.strftime('%Y-%m')
                                month_display = date_val.strftime('%B %Y').capitalize()
                                months.add((month_key, month_display))
                                print(f"Added month: {month_key} - {month_display}")
                        except Exception as e:
                            print(f"Error processing date {date_val}: {e}")
                else:
                    print(f"Column '{date_col_name}' not found in DataFrame")
        except Exception as e:
            print(f"Error processing file {getattr(uploaded_file, 'file', 'unknown')}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n=== get_available_months() complete ===")
    # Convert to list and sort by date (newest first)
    months_list = sorted(list(months), key=lambda x: x[0], reverse=True)
    print(f"Final months list: {months_list}")
    return months_list

def statistique(request):
    # Redirect unauthenticated users to login page
    if not request.user.is_authenticated:
        from django.urls import reverse
        from django.shortcuts import redirect
        return redirect(reverse('login') + '?next=' + request.path)
        
    user = request.user
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        excel_files = UploadedExcel.objects.all()
    else:
        excel_files = UploadedExcel.objects.filter(uploaded_by=user)
        
    # Get available months for the filter
    months = get_available_months()
    print(f"Available months: {months}")
    selected_month = request.GET.get('filter_month_year', '')

    all_records = []
    for uploaded_file in excel_files:
        try:
            df = pd.read_excel(uploaded_file.file.path)
            mapping = {col.lower().strip(): col for col in df.columns}
            
            name_col = mapping.get('name')
            in_col = mapping.get('in')
            out_col = mapping.get('out')
            date_col = mapping.get('date')
            dept_col = mapping.get('département') or mapping.get('department')
            
            if not all([name_col, in_col, out_col, date_col]):
                continue

            for _, row in df.iterrows():
                try:
                    heure_in = str(row[in_col]).strip()
                    heure_out = str(row[out_col]).strip()
                    if not heure_in or not heure_out or heure_in.lower() == 'nan' or heure_out.lower() == 'nan':
                        continue
                    t_in = datetime.strptime(heure_in, '%H:%M') if len(heure_in) <= 5 else datetime.strptime(heure_in, '%H:%M:%S')
                    t_out = datetime.strptime(heure_out, '%H:%M') if len(heure_out) <= 5 else datetime.strptime(heure_out, '%H:%M:%S')
                    duree = (t_out - t_in)
                    if duree < timedelta(0):
                        duree += timedelta(days=1)
                    heures_travaillees = duree.total_seconds() / 3600
                    heures_travaillees_arr = math.ceil(heures_travaillees)
                    date_val = row[date_col]
                    date_obj = None
                    if isinstance(date_val, datetime):
                        date_obj = date_val
                    else:
                        date_str = str(date_val)
                        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%m/%d/%Y"):
                            try:
                                date_obj = datetime.strptime(date_str, fmt)
                                break
                            except Exception:
                                continue
                            if not date_obj:
                                continue
                    if date_obj.weekday() in [5, 6]:
                        heures_sup = heures_travaillees_arr
                    else:
                        heures_sup = max(0, heures_travaillees_arr - 8)
                    if heures_sup > 0:
                        department = str(row[dept_col]) if dept_col and pd.notna(row[dept_col]) else None
                        all_records.append({
                            'nom': str(row[name_col]),
                            'heures_sup': heures_sup,
                            'date_obj': date_obj,
                            'department': department
                        })
                except Exception:
                    continue
        except Exception:
            continue
    
    # Create lists for filters before filtering records
    all_names = sorted(list(set(r['nom'] for r in all_records)))
    
    # Debug: Afficher les enregistrements bruts
    print("\n=== DEBUG: Enregistrements bruts ===")
    for i, r in enumerate(all_records[:5]):  # Afficher les 5 premiers enregistrements
        print(f"Enregistrement {i+1}: {r}")
    
    # Extraire les départements uniques
    all_departments = []
    departments_set = set()
    for r in all_records:
        dept = r.get('department')
        if dept and dept not in departments_set:
            departments_set.add(dept)
            all_departments.append(dept)
    
    all_departments = sorted(all_departments)
    
    print(f"\n=== DEBUG: Départements extraits ===")
    print(f"Nombre total d'enregistrements: {len(all_records)}")
    print(f"Départements uniques ({len(all_departments)}): {all_departments}")
    
    # Préparer les mois disponibles
    available_dates = {r['date_obj'] for r in all_records if r.get('date_obj')}
    unique_year_months = sorted(list(set((d.year, d.month) for d in available_dates)), reverse=True)
    available_months = [(f"{year}-{month:02d}", f"{MONTH_NAMES_FR[month]} {year}") for year, month in unique_year_months]

    # Apply filters
    filter_nom = request.GET.get('filter_nom', '').strip()
    filter_month_year = request.GET.get('filter_month_year', '').strip()
    filter_department = request.GET.get('filter_department', '').strip()

    filtered_records = all_records
    if filter_nom:
        filtered_records = [r for r in filtered_records if r['nom'] == filter_nom]
    if filter_department:
        filtered_records = [r for r in filtered_records if r.get('department') == filter_department]
    if filter_month_year:
        try:
            year, month = map(int, filter_month_year.split('-'))
            filtered_records = [r for r in filtered_records if r.get('date_obj') and r['date_obj'].year == year and r['date_obj'].month == month]
        except ValueError:
            pass

    # Aggregate stats from filtered records
    stats = {}
    dept_stats = {}
    
    for record in filtered_records:
        nom = record['nom']
        dept = record.get('department') or 'Non spécifié'
        
        # Stats par employé
        if nom not in stats:
            stats[nom] = {'total_heures_sup': 0, 'nb_jours': 0, 'department': dept}
        stats[nom]['total_heures_sup'] += record['heures_sup']
        stats[nom]['nb_jours'] += 1
        
        # Stats par département
        if dept not in dept_stats:
            dept_stats[dept] = 0
        dept_stats[dept] += record['heures_sup']

    # Convertir en listes pour le template
    stats_list = [{'nom': nom, 'total_heures_sup': v['total_heures_sup'], 
                  'nb_jours': v['nb_jours'], 'department': v['department']} 
                 for nom, v in stats.items()]
    
    # Trier les départements par heures totales (décroissant)
    dept_stats = dict(sorted(dept_stats.items(), key=lambda item: item[1], reverse=True))

    # Préparer les données pour le graphique
    chart_data = {
        'labels': [s['nom'] for s in stats_list],
        'heuresData': [s['total_heures_sup'] for s in stats_list],
        'joursData': [s['nb_jours'] for s in stats_list],
        'deptLabels': list(dept_stats.keys()),
        'deptHeuresData': list(dept_stats.values())
    }

    # Pagination
    paginator = Paginator(stats_list, 20)  # 20 items per page
    
    # Get page number from request, default to 1
    page_number = request.GET.get('page', 1)
    
    try:
        page = paginator.page(page_number)
        stats_page = page
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    page_obj = paginator.get_page(page_number)

    # Préparer le contexte pour le template
    departments_list = all_departments if 'all_departments' in locals() else []
    
    # Log pour débogage
    print(f"\n=== DEBUG: Contexte transmis au template ===")
    print(f"Nombre de départements: {len(departments_list)}")
    print(f"Départements: {departments_list}")
    print(f"Mois disponibles: {months}")
    
    context = {
        'stats': stats_page,
        'page_obj': page_obj,
        'all_names': all_names,
        'chart_data': chart_data,
        'dept_labels': json.dumps(list(dept_stats.keys())),
        'dept_heures_data': json.dumps(list(dept_stats.values())),
        'filter_nom': filter_nom,
        'filter_department': filter_department,
        'filter_month_year': filter_month_year,
        'months': months,
        'selected_month': selected_month,
        'departments': departments_list,
        'included_files': excel_files,  # Pass the queryset of files to the template
    }

    return render(request, 'pointage/statistique.html', context)

@login_required
def pie_chart_data(request):
    from .models import UploadedExcel
    import pandas as pd
    from datetime import datetime
    from collections import defaultdict

    user = request.user
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        files = UploadedExcel.objects.all()
    else:
        files = UploadedExcel.objects.filter(uploaded_by=user)

    month_filter = request.GET.get('month')
    filter_year = None
    filter_month = None
    if month_filter:
        try:
            year_str, month_str = month_filter.split('-')
            filter_year = int(year_str)
            filter_month = int(month_str.lstrip('0'))  # Remove leading zero if present
        except (ValueError, AttributeError):
            return JsonResponse({'labels': [], 'data': []})

    dept_hours = defaultdict(float)
    for uploaded_file in files:
        try:
            df = pd.read_excel(uploaded_file.file.path)
            mapping = {col.lower().strip(): col for col in df.columns}

            name_col = mapping.get('name')
            in_col = mapping.get('in')
            out_col = mapping.get('out')
            date_col = mapping.get('date')
            dept_col = mapping.get('département') or mapping.get('department')
            
            if not all([name_col, in_col, out_col, date_col]):
                continue

            for _, row in df.iterrows():
                try:
                    heure_in = str(row[in_col]).strip()
                    heure_out = str(row[out_col]).strip()
                    if not heure_in or not heure_out or heure_in.lower() == 'nan' or heure_out.lower() == 'nan':
                        continue
                    t_in = datetime.strptime(heure_in, '%H:%M') if len(heure_in) <= 5 else datetime.strptime(heure_in, '%H:%M:%S')
                    t_out = datetime.strptime(heure_out, '%H:%M') if len(heure_out) <= 5 else datetime.strptime(heure_out, '%H:%M:%S')
                    duree = (t_out - t_in)
                    if duree < pd.Timedelta(0):
                        duree += pd.Timedelta(days=1)
                    heures_travaillees = duree.total_seconds() / 3600
                    heures_travaillees_arr = math.ceil(heures_travaillees)
                    date_val = row[date_col]
                    date_obj = None
                    if isinstance(date_val, datetime):
                        date_obj = date_val
                    else:
                        date_str = str(date_val)
                        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%m/%d/%Y"):
                            try:
                                date_obj = datetime.strptime(date_str, fmt)
                                break
                            except Exception:
                                continue
                        if not date_obj:
                            continue
                    if filter_year and filter_month:
                        # Accept both int and str with/without leading zero
                        if date_obj.year != filter_year or date_obj.month != filter_month:
                            continue
                    if date_obj.weekday() in [5, 6]:
                        heures_sup = heures_travaillees_arr
                    else:
                        heures_sup = max(0, heures_travaillees_arr - 8)
                    if heures_sup > 0:
                        department = str(row[dept_col]) if dept_col and pd.notna(row[dept_col]) else 'Non spécifié'
                        dept_hours[department] += heures_sup
                except Exception:
                    continue
        except Exception:
            continue
    # Sort departments by hours descending
    sorted_depts = sorted(dept_hours.items(), key=lambda x: x[1], reverse=True)
    labels = [dept for dept, _ in sorted_depts]
    data = [round(hours, 2) for _, hours in sorted_depts]
    return JsonResponse({'labels': labels, 'data': data})
