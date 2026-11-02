import sqlite3

# Connect to target on-premise SQLite logging repository
conn = sqlite3.connect('micron_fab4.db')
cursor = conn.cursor()

print("===== LATEST DATASTREAM LOGS (LAST 5 RECORDS) =====")
# Query recent raw history to confirm active high-frequency ingestion matches
cursor.execute("SELECT id, tool_id, chamber_pressure_psi, network_latency_ms FROM telemetry_logs ORDER BY id DESC LIMIT 5")
for row in cursor.fetchall():
    print(f"ID: {row[0]} | Tool: {row[1]} | Pressure: {row[2]} PSI | Latency: {row[3]}ms")

print("\n===== TRIAGED INCIDENT REPORT LOGS =====")
# Extract all historical anomalies captured by the automated FDC engine
cursor.execute("SELECT incident_id, tool_id, fault_type, severity, details FROM system_incidents ORDER BY incident_id DESC")
rows = cursor.fetchall()
if not rows:
    print("No incidents recorded yet. All systems operating within standard safety limits.")
else:
    for row in rows:
        print(f"Incident: {row[0]} | Tool: {row[1]} | Type: {row[2]} | Severity: {row[3]} | Details: {row[4]}")

conn.close()
