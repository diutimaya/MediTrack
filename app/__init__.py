from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config

db             = SQLAlchemy()
login_manager  = LoginManager()
bcrypt         = Bcrypt()
task_scheduler = BackgroundScheduler()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions
    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Register blueprints — imported HERE to avoid circular imports
    from app.routes.auth      import auth_bp
    from app.routes.medicines import medicines_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.stock     import stock_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(medicines_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(stock_bp)

    # Create tables, then start scheduler
    with app.app_context():
        db.create_all()

        if not task_scheduler.running:
            from app.scheduler.jobs import remind_job, stock_alert_job
            task_scheduler.add_job(
                func=remind_job,
                args=[app],
                trigger="interval",
                seconds=app.config["REMINDER_CHECK_INTERVAL_SECONDS"],
                id="remind_job",
                replace_existing=True,
            )
            task_scheduler.add_job(
                func=stock_alert_job,
                args=[app],
                trigger="interval",
                minutes=app.config["LOW_STOCK_CHECK_INTERVAL_MINUTES"],
                id="stock_alert_job",
                replace_existing=True,
            )
            task_scheduler.start()

    return app