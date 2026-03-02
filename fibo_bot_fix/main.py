#!/usr/bin/env python3
"""
Point d'entrée du Forex Fibonacci Bot - Compatible python-telegram-bot v20+

Usage:
    python main.py
    
Les variables d'environnement doivent être définies:
    - TELEGRAM_TOKEN_FIBOBOT
    - TWELVEDATA_API_KEY_FIBOBOT
"""

import asyncio
import signal
import sys
import os
from threading import Thread
from flask import Flask
from telegram.ext import Application, CommandHandler
from config.secrets import Secrets
from config.settings import PAIRS
from data.twelvedata_client import TwelveDataClient
from data.database import Database
from bot.handlers import CommandHandlers
from scheduler.jobs import SchedulerManager
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Flask app pour UptimeRobot (keep-alive)
flask_app = Flask(__name__)


@flask_app.route('/')
def health_check():
    """Endpoint pour UptimeRobot"""
    return {'status': 'ok', 'bot': 'running'}, 200


@flask_app.route('/health')
def health():
    """Endpoint santé"""
    return {'status': 'healthy'}, 200


class FiboBotApplication:
    """Application principale du bot Fibonacci"""

    def __init__(self):
        """Initialiser l'application"""
        self.api_client = None
        self.db = None
        self.scheduler_manager = None
        self.application = None
        self.chat_id = None
        self.flask_thread = None
        self.running = False

    async def initialize(self):
        """Initialiser tous les composants"""
        try:
            logger.info("🚀 Initialisation du Forex Fibonacci Bot...")

            # Initialiser les secrets
            telegram_token = Secrets.get_telegram_token()
            twelvedata_key = Secrets.get_twelvedata_api_key()

            logger.info(f"✅ Secrets chargés")

            # Initialiser le client API
            self.api_client = TwelveDataClient(twelvedata_key)
            logger.info(f"✅ Client Twelve Data initialisé")

            # Initialiser la base de données
            self.db = Database("fibo_bot.db")
            logger.info(f"✅ Base de données initialisée")

            # Initialiser le bot Telegram avec la nouvelle API v20+
            self.application = (
                Application.builder()
                .token(telegram_token)
                .build()
            )
            logger.info(f"✅ Bot Telegram configuré (v20+)")

            # Initialiser les handlers
            handlers = CommandHandlers(self.db)

            self.application.add_handler(CommandHandler("start", handlers.handle_start))
            self.application.add_handler(CommandHandler("status", handlers.handle_status))
            self.application.add_handler(CommandHandler("pairs", handlers.handle_pairs))
            self.application.add_handler(CommandHandler("history", handlers.handle_history))
            self.application.add_handler(CommandHandler("stats", handlers.handle_stats))

            self.application.add_error_handler(handlers.handle_error)

            logger.info(f"✅ Handlers Telegram configurés")

            # Pour les tests, utiliser un chat_id par défaut
            # En production, ce serait configuré différemment
            self.chat_id = 0  # À remplacer par l'ID du chat réel

            # Initialiser le scheduler
            self.scheduler_manager = SchedulerManager(
                self.api_client,
                self.db,
                self.application,
                self.chat_id,
            )
            scheduler = self.scheduler_manager.setup()
            logger.info(f"✅ Scheduler configuré")

            logger.info(f"✅ Bot Fibonacci initialisé avec succès!")
            logger.info(f"📊 Paires surveillées: {', '.join(PAIRS)}")
            logger.info(f"💾 Crédits API: {self.api_client.get_credits_remaining()}/800")

            return True

        except Exception as e:
            logger.error(f"❌ Erreur initialisation: {e}", exc_info=True)
            return False

    def start_flask(self):
        """Démarrer le serveur Flask dans un thread séparé"""
        try:
            port = int(os.getenv("PORT", 10000))
            logger.info(f"🌐 Démarrage serveur Flask sur port {port}")
            flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False, threaded=True)
        except Exception as e:
            logger.error(f"❌ Erreur Flask: {e}", exc_info=True)

    async def start(self):
        """Démarrer le bot"""
        try:
            if not await self.initialize():
                logger.error("Impossible d'initialiser le bot")
                return False

            logger.info("🎯 Démarrage du bot...")

            # Démarrer le serveur Flask dans un thread séparé
            self.flask_thread = Thread(target=self.start_flask, daemon=True)
            self.flask_thread.start()
            logger.info("✅ Serveur Flask démarré")

            # Démarrer le scheduler
            self.scheduler_manager.start()
            logger.info("✅ Scheduler démarré")

            # Démarrer le bot Telegram avec la nouvelle API v20+
            self.running = True
            logger.info("✅ Application Telegram initialisée")
            logger.info("✅ Application Telegram démarrée")
            logger.info("🎯 Démarrage du polling...")
            
            # Utiliser run_polling() avec async context manager
            async with self.application:
                await self.application.run_polling(
                    allowed_updates=["message", "callback_query"]
                )

        except Exception as e:
            logger.error(f"❌ Erreur démarrage: {e}", exc_info=True)
            return False

    async def stop(self):
        """Arrêter le bot"""
        try:
            logger.info("🛑 Arrêt du bot...")
            self.running = False

            if self.scheduler_manager:
                self.scheduler_manager.stop()

            logger.info("✅ Bot arrêté")

        except Exception as e:
            logger.error(f"❌ Erreur arrêt: {e}", exc_info=True)



async def main():
    """Fonction principale"""
    app = FiboBotApplication()
    
    # Démarrer le bot
    success = await app.start()
    
    if not success:
        logger.error("❌ Échec du démarrage du bot")
        return
    
    # Garder le programme en vie jusqu'à ce que le bot s'arrête
    try:
        while app.running:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot arrêté par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}", exc_info=True)
        sys.exit(1)
