@echo off
REM Script de démarrage du serveur Django

echo ========================================
echo Facturation - Django Invoice Management
echo ========================================
echo.

REM Activation de l'environnement virtuel
echo Activation de l'environnement virtuel...
call invoice_env\Scripts\activate.bat

REM Vérification des migrations
echo.
echo Application des migrations de base de données...
python manage.py migrate --noinput

REM Création de l'utilisateur admin (s'il n'existe pas)
echo.
echo Vérification de l'utilisateur admin...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" 2>nul

REM Lancement du serveur
echo.
echo ========================================
echo Démarrage du serveur...
echo ========================================
echo.
echo 🌐 Accédez à:
echo   - Dashboard: http://127.0.0.1:8000/
echo   - Admin: http://127.0.0.1:8000/admin/
echo   - API: http://127.0.0.1:8000/api/v1/
echo.
echo 🔐 Identifiants:
echo   - Username: admin
echo   - Password: admin
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo ========================================
echo.

python manage.py runserver 0.0.0.0:8000

pause
