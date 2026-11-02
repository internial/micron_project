import time
import json
import random
import sys

print("SECS/GEM Equipment Simulator active. Initiating Fab 4 tool telemetry stream...", file=sys.stderr)

while True:
    # Generate realistic float values mirroring an active production chamber
    data = {
        "timestamp": int(time.time()),
        "tool_id": f"FAB4-ETCH-0{random.randint(1, 3)}",
        "chamber_pressure_psi": round(random.uniform(14.0, 16.5), 2),
        "network_latency_ms": round(random.uniform(1.1, 9.2), 2),
        "packet_drop_status": random.choices([0, 1], weights=[0.90, 0.10])[0]
    }
    
    # Prepend a simulated industrial SECS protocol communication header string
    protocol_packet = f"SECS_DATA_STREAM|{json.dumps(data)}"
    
    # Flush data straight to the terminal standard output stream for processing
    print(protocol_packet)
    sys.stdout.flush()
    
    # Emit a fresh metric package precisely every single second
    time.sleep(1)
