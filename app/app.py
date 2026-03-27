import os
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from app.database import add_feedback, init_db, list_feedback


def create_app(db_path: str | None = None) -> Flask:
    project_root = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )

    resolved_db_path = db_path or os.getenv("DATABASE_PATH", str(project_root / "data" / "feedback.db"))
    app.config["DATABASE_PATH"] = resolved_db_path

    init_db(app.config["DATABASE_PATH"])

    @app.route("/", methods=["GET"])
    def index():
        recent_feedback = list_feedback(app.config["DATABASE_PATH"], limit=10)
        return render_template("index.html", feedback_entries=recent_feedback)

    @app.route("/submit", methods=["POST"])
    def submit_feedback():
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not message:
            recent_feedback = list_feedback(app.config["DATABASE_PATH"], limit=10)
            error = "Both name and feedback are required."
            return render_template("index.html", feedback_entries=recent_feedback, error=error), 400

        add_feedback(app.config["DATABASE_PATH"], name, message)
        return redirect(url_for("index"))

    @app.route("/feedback", methods=["GET"])
    def feedback():
        all_feedback = list_feedback(app.config["DATABASE_PATH"])
        return render_template("feedback.html", feedback_entries=all_feedback)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
