from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Simple in-memory store (not persistent)
_items = []
_next_id = 1


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "FlaskAPP-python-container",
        "description": "Simple example Flask API (in-memory)",
        "endpoints": ["/ping", "/items"]
    })


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})


@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(_items)


@app.route("/items", methods=["POST"])
def create_item():
    global _next_id
    if not request.is_json:
        return jsonify({"error": "expected application/json"}), 400
    payload = request.get_json()
    name = payload.get("name")
    if not name:
        return jsonify({"error": "missing field 'name'"}), 400
    item = {"id": _next_id, "name": str(name)}
    _items.append(item)
    _next_id += 1
    return jsonify(item), 201


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id: int):
    for it in _items:
        if it["id"] == item_id:
            return jsonify(it)
    return jsonify({"error": "not found"}), 404


@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id: int):
    if not request.is_json:
        return jsonify({"error": "expected application/json"}), 400
    payload = request.get_json()
    name = payload.get("name")
    if name is None:
        return jsonify({"error": "missing field 'name'"}), 400
    for it in _items:
        if it["id"] == item_id:
            it["name"] = str(name)
            return jsonify(it)
    return jsonify({"error": "not found"}), 404


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id: int):
    for i, it in enumerate(_items):
        if it["id"] == item_id:
            _items.pop(i)
            return jsonify({"deleted": item_id})
    return jsonify({"error": "not found"}), 404


if __name__ == "__main__":
    # Only for local development; container uses Gunicorn
    app.run(host="0.0.0.0", port=5000, debug=True)
