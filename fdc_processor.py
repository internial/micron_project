import sys
import json
import sqlite3
import datetime

print("PCS FDC Processor Online. Awaiting incoming SECS data blocks...", file=sys.stderr)

# Read continuous incoming data blocks line-by-line via terminal input
for line in sys.stdin:
    raw_line = line.strip()
    if not raw_line or "SECS_DATA_STREAM|" not in raw_line:
        continue
        
    try:
        # Protocol Unpacking: Split away communication header to isolate JSON payload
        payload_str = raw_line.split("SECS_DATA_STREAM|")
        metric = json.loads(payload_str[1])
        
        # Open operational connection to local data repository instance
        conn = sqlite3.connect('micron_fab4.db')
        cursor = conn.cursor()
        
        # Write comprehensive metrics packet directly to telemetry tables
        cursor.execute('''
            INSERT INTO telemetry_logs (timestamp, tool_id, chamber_pressure_psi, network_latency_ms, packet_drop_status)
            VALUES (?, ?, ?, ?, ?)
        ''', (metric["timestamp"], metric["tool_id"], metric["chamber_pressure_psi"], metric["network_latency_ms"], metric["packet_drop_status"]))
        
        pressure = metric["chamber_pressure_psi"]
        latency = metric["network_latency_ms"]
        drop = metric["packet_drop_status"]
        tool = metric["tool_id"]
        
        # FDC Automation Rule A: Evaluate and handle critical chamber pressure limits
        if pressure > 16.0:
            cursor.execute('''
                INSERT INTO system_incidents (timestamp, tool_id, fault_type, severity, details)
                VALUES (?, ?, 'PRESSURE_EXCURSION', 'CRITICAL', ?)
            ''', (metric["timestamp"], tool, f"Chamber pressure spiked to safe ceiling limit at {pressure} PSI"))
            print(f"[{datetime.datetime.now()}] 🚨 FDC FAULT DETECTED: Critical pressure breach on {tool} ({pressure} PSI)")
            
        # FDC Automation Rule B: Evaluate and handle transport interface network degradation
        elif latency > 8.0 or drop == 1:
            cursor.execute('''
                INSERT INTO system_incidents (timestamp, tool_id, fault_type, severity, details)
                VALUES (?, ?, 'INTERFACE_DEGRADATION', 'WARNING', ?)
            ''', (metric["timestamp"], tool, f"Connection latency spiked to {latency}ms | Drop status: {drop}"))
            print(f"[{datetime.datetime.now()}] ⚠️ FDC WARNING: Intermittent transport lag caught on {tool} ({latency}ms)")
            
        # Log standard baseline message if all parameters clear safety bounds
        else:
            print(f"[{datetime.datetime.now()}] Log Recorded: {tool} status normal. Pressure: {pressure} PSI | Latency: {latency}ms")
            
        # Commit transactional modifications and disconnect safely
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"FDC Pipeline Parsing Exception occurred: {e}", file=sys.stderr)
