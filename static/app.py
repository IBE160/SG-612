from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# midlertidig "database" i minnet til vi kobler på SQLite
TASKS = [
    {"id": 1, "title": "Kjøpe melk", "label": "Home", "priority": "low", "is_done": False},
    {"id": 2, "title": "Øve til prøve", "label": "School", "priority": "high", "is_done": False},
]

@app.route("/")
def index():
    # sortér slik at high vises først – bare for demo
    prio_order = {"high": 0, "medium": 1, "low": 2}
    tasks = sorted(TASKS, key=lambda t: prio_order.get(t["priority"], 3))
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if not title:
        return redirect(url_for("index"))

    new_id = (max([t["id"] for t in TASKS]) + 1) if TASKS else 1

    TASKS.append({
        "id": new_id,
        "title": title,
        "label": request.form.get("label", "Other"),
        "priority": request.form.get("priority", "low"),
        "is_done": False,
    })
    return redirect(url_for("index"))

@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    for t in TASKS:
        if t["id"] == task_id:
            t["is_done"] = not t["is_done"]
            break
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

