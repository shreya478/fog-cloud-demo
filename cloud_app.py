from flask import Flask, request, jsonify
import time

app = Flask(__name__)
store = []

@app.post("/ingest")
def ingest():
    body = request.json
    p = body["payload"]
    mode = body["mode"]
    if mode == "fog":
        alert = body.get("alert", False)       # fog already decided locally
    else:
        alert = p.get("hr", 0) > 120 or p.get("spo2", 100) < 90   # cloud decides
    store.append({"t": time.strftime("%H:%M:%S"), "mode": mode, "data": p, "alert": alert})
    return jsonify(ok=True, alert=alert)

@app.get("/")
def view():
    rows = "".join(
        f"<tr><td>{s['t']}</td><td>{s['mode']}</td><td>{s['data']}</td><td>{s['alert']}</td></tr>"
        for s in store[-20:][::-1])
    return ("<meta http-equiv='refresh' content='3'>"
            "<h2>Cloud storage: what the cloud sees</h2>"
            "<table border=1 cellpadding=6><tr><th>Time</th><th>Mode</th><th>Data</th><th>Alert</th></tr>"
            f"{rows}</table>")