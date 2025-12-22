#!/bin/bash

echo "========================================"
echo "Facturation - Django Invoice Management"
echo "========================================"
echo ""

# Activation de l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source invoice_env/bin/activate

# Application des migrations
echo ""
echo "Application des migrations de base de données..."
python manage.py migrate --noinput

# Création de l'utilisateur admin
echo ""
echo "Vérification de l'utilisateur admin..."
python manage.py shell <<EOF 2>/dev/null
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Utilisateur admin créé")
else:
    print("Utilisateur admin existe déjà")
EOF

# Lancement du serveur
echo ""
echo "========================================"
echo "Démarrage du serveur..."
echo "========================================"
echo ""
echo "🌐 Accédez à:"
echo "   - Dashboard: http://127.0.0.1:8000/"
echo "   - Admin: http://127.0.0.1:8000/admin/"
echo "   - API: http://127.0.0.1:8000/api/v1/"
echo ""
echo "🔐 Identifiants:"
echo "   - Username: admin"
echo "   - Password: admin"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo "========================================"
echo ""

python manage.py runserver 0.0.0.0:8000
