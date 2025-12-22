# 🚀 Comment Lancer le Site

## Option 1: Lancer le Script (RECOMMANDÉ) ⭐

### Windows:
```bash
double-cliquez sur run.bat
```

Ou en terminal:
```bash
run.bat
```

### Linux/Mac:
```bash
bash run.sh
```

Ou:
```bash
chmod +x run.sh
./run.sh
```

Le script va:
- ✅ Activer l'environnement virtuel
- ✅ Appliquer les migrations de BD
- ✅ Créer l'utilisateur admin (admin/admin)
- ✅ Démarrer le serveur

---

## Option 2: Commandes Manuelles

### 1️⃣ Activer l'environnement

**Windows (PowerShell):**
```powershell
invoice_env\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
invoice_env\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source invoice_env/bin/activate
```

### 2️⃣ Appliquer les migrations
```bash
python manage.py migrate
```

### 3️⃣ Créer un utilisateur admin
```bash
python manage.py createsuperuser
```

Suivez les prompts (username: `admin`, password: `admin`)

### 4️⃣ Lancer le serveur
```bash
python manage.py runserver
```

---

## ✅ Le Serveur est Lancé!

Vous devriez voir:
```
Starting development server at http://127.0.0.1:8000/
```

---

## 🌐 URLs d'Accès

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/ | Page d'accueil/Dashboard |
| http://127.0.0.1:8000/admin/ | Panel d'administration |
| http://127.0.0.1:8000/api/v1/ | API REST |
| http://127.0.0.1:8000/login/ | Page de connexion |

---

## 🔐 Identifiants par Défaut

**Username:** `admin`  
**Password:** `admin`

⚠️ Changez le mot de passe après la première connexion!

---

## 📋 Qu'est-ce que je peux faire?

### Dashboard
- Voir les métriques clés (total facturé, payé, en attente, en retard)
- Affichage des factures récentes
- Affichage des paiements récents
- Affichage des produits en rupture de stock

### Facturation
- Lister toutes les factures
- Voir les détails d'une facture
- Filtrer par statut, client, date
- Exporter en PDF/Excel
- Marquer comme payée

### Clients
- Lister les clients
- Voir détails et statistiques
- Historique des factures

### Produits
- Lister les produits
- Voir les stocks
- Alertes de rupture

### Fournisseurs
- Lister les fournisseurs
- Détails de contact

### Paiements
- Lister tous les paiements
- Historique par facture

---

## ⚠️ Problèmes Courants

### "Port 8000 déjà utilisé"
```bash
python manage.py runserver 8001
```

### "ModuleNotFoundError"
Assurez-vous que l'environnement est activé:
```bash
# Windows
invoice_env\Scripts\activate.bat

# Linux/Mac
source invoice_env/bin/activate
```

### "Database locked"
Supprimez `db.sqlite3` et relancez:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### "Cannot access /admin"
Assurez-vous que vous êtes connecté avec un compte superuser.

---

## 🛑 Arrêter le Serveur

Appuyez sur **Ctrl+C** dans le terminal

---

## 📚 Documentation

- **QUICK_START.md** - Guide rapide
- **README.md** - Présentation complète
- **PROJECT_SETUP.md** - Configuration technique
- **API_DOCUMENTATION.md** - Documentation API

---

## ✨ Prochaines Étapes

1. **Connectez-vous** avec `admin` / `admin`
2. **Explorez l'interface**
3. **Créez des données** (Clients, Produits, Factures)
4. **Testez les exports** (PDF/Excel)
5. **Consultez l'API** via http://127.0.0.1:8000/api/v1/

---

**Bon travail! 🎉**
