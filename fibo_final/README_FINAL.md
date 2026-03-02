# 🤖 Forex Fibonacci Bot - Version Finale

Bot Telegram de trading Forex automatisé utilisant une stratégie multi-timeframe (Weekly/Daily/H1) avec retracements de Fibonacci, SMA 200, et bougies Heiken Ashi.

## 🎯 Fonctionnalités

✅ **Stratégie Fibonacci 4-niveaux**
- Détecte jusqu'à 4 niveaux de retracement simultanément
- Signaux BULLISH et BEARISH
- Analyse multi-timeframe (W1 → D1 → H1)

✅ **Indicateurs Techniques**
- SMA 200 pour filtrage de tendance
- Bougies Heiken Ashi pour confirmation
- RSI pour divergences
- Support/Résistance

✅ **Notifications Telegram**
- Signaux en temps réel
- Alertes prix dans zone Fibonacci
- Résumé quotidien des paires alignées

✅ **14 Paires Forex Surveillées**
EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, NZD/USD, EUR/GBP, EUR/JPY, GBP/JPY, AUD/JPY, EUR/CHF, GBP/CHF, CAD/JPY

## 🚀 Déploiement Rapide

### Sur Render (Recommandé)

1. **Créer un nouveau service** : https://render.com
2. **Connecter ce repository**
3. **Ajouter les variables d'environnement** :
   - `TELEGRAM_TOKEN_FIBOBOT` : Votre token Telegram
   - `TWELVEDATA_API_KEY_FIBOBOT` : Votre clé API Twelve Data
4. **Déployer** : Render redéploiera automatiquement à chaque push

👉 **Guide détaillé** : Voir `SETUP_RENDER.md`

### Localement

```bash
# 1. Cloner le repository
git clone <votre_repo>
cd fibo_bot

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos tokens

# 4. Démarrer le bot
python main.py
```

## 📊 Commandes Telegram

| Commande | Description |
|----------|-------------|
| `/start` | Démarrer le bot |
| `/status` | Statut des paires alignées |
| `/pairs` | Statut détaillé des 14 paires |
| `/history` | Derniers signaux (24h) |
| `/stats` | Performance (weekend uniquement) |

## 🔧 Architecture

```
fibo_bot/
├── main.py              # Point d'entrée
├── bot/                 # Handlers Telegram
├── core/                # Logique Fibonacci
├── data/                # API Twelve Data
├── scheduler/           # Jobs automatiques
├── config/              # Configuration
└── utils/               # Utilitaires
```

## 📈 Scans Automatiques

- **Weekly (W1)** : Chaque lundi 00:00 UTC
- **Daily (D1)** : Chaque jour 00:00 UTC
- **Hourly (H1)** : Chaque heure (horaires de trading)

## ⚙️ Configuration

Éditer `config/settings.py` pour :
- Ajouter/retirer des paires
- Modifier les horaires de scan
- Ajuster les paramètres Fibonacci

## 🐛 Dépannage

### Le bot ne démarre pas
```bash
# Vérifier les logs
tail -f logs/bot.log

# Vérifier les variables d'environnement
echo $TELEGRAM_TOKEN_FIBOBOT
echo $TWELVEDATA_API_KEY_FIBOBOT
```

### Erreur "Updater"
Cette version corrige ce problème. Si vous la voyez, supprimez le service Render et recréez-le.

### Pas de signaux
1. Vérifier que les paires ont des données disponibles
2. Vérifier les crédits API Twelve Data
3. Vérifier les logs pour les erreurs

## 📝 Notes Importantes

- **UptimeRobot** : Non nécessaire, Render gère l'uptime automatiquement
- **Plan Free Render** : Service s'endort après 15 min d'inactivité (normal)
- **Plan Premium Render** : Service 24/7 sans interruption
- **Crédits API** : Twelve Data = 800 crédits/jour (suffisant pour 14 paires)

## 📞 Support

Pour les problèmes :
1. Vérifier les logs Render
2. Vérifier les variables d'environnement
3. Vérifier la documentation technique (DOC_TECHNIQUE.md)

## 📄 Licence

Propriétaire - Utilisation personnelle uniquement

---

**Version** : 1.0 Final
**Dernière mise à jour** : 02/03/2026
**Status** : ✅ Production Ready
