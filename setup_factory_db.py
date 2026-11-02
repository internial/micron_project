import sqlite3

# Connect or create the local SQLite database file
conn = sqlite3.connect('micron_fab4.db')
cursor = conn.cursor()

# Table 1: Store continuous, high-frequency machine telemetry history
cursor.execute('''
    CREATE TABLE IF NOT EXISTS telemetry_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER,
        tool_id TEXT,
        chamber_pressure_psi REAL,
        network_latency_ms REAL,
        packet_drop_status INTEGER
    )
''')

# Table 2: Store prioritized, triaged incident logs for engineering teams
cursor.execute('''
    CREATE TABLE IF NOT EXISTS system_incidents (
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER,
        tool_id TEXT,
        fault_type TEXT,
        severity TEXT,
        details TEXT
    )
''')

# Commit database structural schema changes and close connection safely
conn.commit()
conn.close()
print("Database schema deployed successfully into micron_fab4.db.")
