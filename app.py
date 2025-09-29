from pathlib import Path

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "amount": self.amount}


def create_app():

    Path("instance").mkdir(parents=True, exist_ok=True)
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Health checkpoint
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.route("/orders", methods=["GET", "POST"])
    def orders():
        if request.method == "GET":
            rows = Order.query.all()
            return jsonify([o.to_dict() for o in rows]), 200

        data = request.get_json(silent=True) or {}
        amount = data.get("amount")
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except Exception:
            return jsonify({"error": "amount must be a positive number"}), 400

        o = Order(amount=amount)
        db.session.add(o)  # create new order in db
        db.session.commit()  # commit new changes
        return jsonify(o.to_dict()), 201

    @app.get("/orders/<int:order_id>")
    def get_order(order_id):
        o = Order.query.get_or_404(
            order_id)
        return jsonify(o.to_dict()), 200

    @app.delete("/orders/<int:order_id>")
    def delete_order(order_id):
        o = Order.query.get(order_id)
        if not o:
            return jsonify({"error": f"Order {order_id} not found"}), 404

        try:
            db.session.delete(o)
            db.session.commit()
            return jsonify({"message": f"Order {order_id} deleted"}), 200
        except Exception:
            db.session.rollback()
            return jsonify({"error": "failed to delete order"}), 500

    @app.get("/")  # Defines a route for the root URL (http://127.0.0.1:5000/).
    def orders_ui():
        rows = Order.query.all()
        return render_template("orders.html", orders=rows)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
