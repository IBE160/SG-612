from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Superenkel "database" i minnet
TASKS = []  # hver task: {"title": str, "label": str, "priority": int}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", tasks=TASKS)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    label = request.form.get("label", "Other")
    # midlertidig: fast prioritet 3 til vi lager heuristikk (fase 1)
    priority = int(request.form.get("priority", 3) or 3)
    if title:
        TASKS.append({"title": title, "label": label, "priority": priority})
    return redirect(url_for("home"))

@app.route("/clear", methods=["POST"])
def clear():
    TASKS.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
