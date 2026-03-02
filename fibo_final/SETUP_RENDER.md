# 🚀 Déploiement sur Render - Guide Complet

## ✅ Prérequis
- Compte Render (https://render.com)
- Token Telegram Bot
- Clé API Twelve Data

## 📋 Étapes de Déploiement

### 1️⃣ Créer un nouveau service sur Render

1. Allez sur https://dashboard.render.com
2. Cliquez sur **"New +"** → **"Web Service"**
3. Connectez votre repository GitHub
4. Sélectionnez ce repository

### 2️⃣ Configurer le service

| Paramètre | Valeur |
|-----------|--------|
| **Name** | `fibo-bot` (ou votre nom) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python main.py` |
| **Plan** | Free (ou Premium si vous voulez 24/7) |

### 3️⃣ Ajouter les variables d'environnement

Allez dans **Settings** → **Environment** et ajoutez :

```
TELEGRAM_TOKEN_FIBOBOT=votre_token_telegram
TWELVEDATA_API_KEY_FIBOBOT=votre_cle_api
PORT=10000
```

### 4️⃣ Déployer

Cliquez sur **"Create Web Service"** et attendez le déploiement (2-3 minutes).

## 🔄 Redéployer après des changements

```bash
git add -A
git commit -m "Fix: description du changement"
git push origin main
```

Render redéploiera automatiquement.

## ⚠️ Important

- **Ne pas utiliser UptimeRobot** : Render garde les services actifs automatiquement
- **Plan Free** : Le service s'endort après 15 minutes d'inactivité (normal)
- **Plan Premium** : Service 24/7 sans interruption
- **Logs** : Allez dans le dashboard Render pour voir les logs en temps réel

## 🐛 Dépannage

### Le bot ne démarre pas
1. Vérifiez les logs : Dashboard → Logs
2. Vérifiez les variables d'environnement
3. Vérifiez que le token Telegram est correct

### Erreur "Updater" 
Cette version corrige ce problème. Si vous la voyez, supprimez le service et recréez-le.

### Le bot s'endort
C'est normal sur le plan Free. Passez au plan Premium pour 24/7.

## 📊 Monitoring

Allez dans **Dashboard** → **Metrics** pour voir :
- Uptime
- CPU usage
- Memory usage
- Network I/O

## ✨ Succès !

Une fois déployé, le bot devrait :
- ✅ Démarrer sans erreur
- ✅ Scanner les paires Forex toutes les heures (H1)
- ✅ Envoyer des notifications Telegram
- ✅ Rester actif 24/7 (sauf plan Free)
