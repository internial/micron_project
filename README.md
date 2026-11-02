# Industry 4.0 Semiconductor Manufacturing Control Pipeline & FDC Engine

A self-contained data infrastructure pipeline designed for advanced manufacturing environments. This system models a headless backend infrastructure that ingests continuous equipment status logs, simulates industrial messaging rules, and executes real-time triage alerts to maximize factory uptime.

## 🏗️ System Architecture

```text
+-------------------------------------------------------------------------+

|                  Layer 1: Equipment Emulation Layer                    |
|                        (tool_simulator.py)                              |
|  - Loops indefinitely (1Hz clock cycle)                                 |
|  - Simulates dynamic chamber environment sensors                        |
|  - Encapsulates payload with proprietary GEM/SECS framing protocol      |
+-------------------------------------------------------------------------+
                                    |
            [ Linux Standard Stream Routing: Terminal Pipe ( | ) ]
                                    v
+-------------------------------------------------------------------------+

|                    Layer 2: Real-Time FDC Engine                        |
|                         (fdc_processor.py)                              |
|  - Listens via standard input stream (sys.stdin)                        |
|  - Performs protocol string parsing & header validation                 |
|  - Validates active hardware metrics against operational safety bounds  |
+-------------------------------------------------------------------------+

            |                               |                        |
     (Clear Metrics)              (Pressure Excursion)      (Network Lag / Drops)

            |                               |                        |
            v                               v                        v
+-----------------------+       +--------------------------------------------+

|     Database Table:   |       |               Database Table:              |
|     telemetry_logs    |       |               system_incidents             |
|                       |       |                                            |
| Logs continuous plant |       | Catalogs prioritized operational exceptions|
| history for SPC analysis      | with exact timestamps for rapid maintenance|
+-----------------------+       +--------------------------------------------+
            \                               /
             \                             /
              v                           v
     +---------------------------------------------+

     | Permanent Relational Storage Core           |
     |              (micron_fab4.db)               |
     +---------------------------------------------+
```

## 📋 Detailed Functional Scope

This architecture acts as an on-premise automated control hub. By avoiding bloated web layers, it proves foundational competencies in system processes, back-end scripting, text stream parsing, and transactional database isolation.

### 1. Equipment Emulation (GEM/SECS Simulation)
Physical semiconductor tools converse with host systems through structured protocol packets. This pipeline simulates that behavior by generating serialized string payloads prefixed with a custom interface wrapper (`SECS_DATA_STREAM|`). The payload alternates randomly across three simulated tools (`FAB4-ETCH-01`, `02`, and `03`) to mimic a parallel production line.

### 2. Fault Detection and Classification (FDC) Logic
The tracking application functions as a first-line automated safety inspector, executing algorithmic validation queries across the active text stream. It interprets data points instantly and branches into three discrete tracks:
*   **Rule A: Pressure Ceiling Enforcement:** Monitors chamber pressure. If vacuum integrity slips and pressure breaches **16.0 PSI**, the tool flags an immediate product risk. It skips normal queues, issues a critical console alarm, and writes a diagnostic record to the incident tracking table to isolate the machine.
*   **Rule B: Interface Degradation Catch:** Monitors communication latency and packet state. If response lag climbs past **8.0ms** or an explicit packet drop status (`1`) is identified, it logs a system warning to alert the network maintenance team before a hard hardware timeout occurs.
*   **Baseline Ingestion:** Healthy packets bypass the incident logging tables and stream directly into the historical log ledger, building a pristine time-series data set ready for long-term tracking analysis.

---

## 💾 Telemetry Data Schema & Payload Formats

### Raw Inbound Protocol Message
```text
SECS_DATA_STREAM|{"timestamp": 1793649850, "tool_id": "FAB4-ETCH-02", "chamber_pressure_psi": 14.85, "network_latency_ms": 3.42, "packet_drop_status": 0}
```

### Decoupled JSON Properties

| Attribute | Data Type | Operational Purpose / Definition |
| :--- | :--- | :--- |
| `timestamp` | Integer | Unix epoch format tracking the exact millisecond of tool data generation. |
| `tool_id` | String | Unique hardware alphanumeric string identifying the specific cleanroom machine station. |
| `chamber_pressure_psi` | Float | Live pressure sensor telemetry measuring vacuum stability inside the wafer chamber. |
| `network_latency_ms` | Float | Measure of data transport delay between the local tool gateway and the processing layer. |
| `packet_drop_status` | Integer | Binary boolean flag (0 = Safe, 1 = Data Drop Encountered) signaling network loss. |

---

## 📺 Live Runtime Demonstration
Watch the live execution, high-frequency stream tracking, and autonomous error routing loops running inside the native console environment:  
👉 **[Micron Fab Simulation & Triage Demo (YouTube)](https://youtube.com)**

---

## 🛠️ Tech Stack & Justification

*   **Python 3:** Handles high-velocity string parsing, data dictionary translations, and threshold evaluation blocks cleanly without execution lag.
*   **Linux/Unix Stream Piping (`|`):** Bypasses the overhead of standard web network protocols (HTTP/REST) by binding process outputs directly to tracking inputs, replicating true headless data distribution architectures.
*   **SQLite Relational Engine:** Provides an on-premise structured file repository matching enterprise SQL syntax (Microsoft SQL Server/Oracle) while running entirely offline inside a single directory with zero configuration footprint.
*   **Zero-Dependency Design:** Written purely via built-in libraries (`sys`, `time`, `json`, `sqlite3`, `datetime`) to guarantee absolute environment portability and immediate execution on any terminal node.

---

## 📋 System Log Signatures

### 1. Normal Operations (Primes Data History Ledger)
```text
[2026-11-02 13:30:01] Log Recorded: FAB4-ETCH-03 status normal. Pressure: 14.52 PSI | Latency: 3.12ms
[2026-11-02 13:30:02] Log Recorded: FAB4-ETCH-01 status normal. Pressure: 15.10 PSI | Latency: 2.85ms
```

### 2. Rule A Triggered (Critical Structural Breach)
```text
[2026-11-02 13:30:05] 🚨 FDC FAULT DETECTED: Critical pressure breach on FAB4-ETCH-02 (16.42 PSI)
```

### 3. Rule B Triggered (Network Interface Degradation Warning)
```text
[2026-11-02 13:30:09] ⚠️ FDC WARNING: Intermittent transport lag caught on FAB4-ETCH-01 (8.75ms)
```

---

## 🚀 Pipeline Lifecycle Instructions

### 1. Launching the System
Execute this single bash configuration file to deploy your relational table structures and instantly kick off the active streaming monitoring dashboard:
```bash
bash start_fab4.sh
```

### 2. Shutting Down the System
To stop the continuous, infinite factory data generation loop safely without causing schema corruption or uncommitted row loss, execute a standard process kill sequence:
```bash
Ctrl + C
```

### 3. Querying the Permanent Audit Logs
To confirm transaction integrity and display a clean analytics summary table of every single anomaly caught by your FDC engine, run the reporting database utility:
```bash
python3 verify_logs.py
```

---

## 📂 Repository File Index
*   `start_fab4.sh`: Simple bash shell automation entry point script.
*   `setup_factory_db.py`: Configures local relational database schemas and storage schemas.
*   `tool_simulator.py`: Manages high-frequency device emulation and string packet wrapping.
*   `fdc_processor.py`: Serves as the core analytical tracking script enforcing production boundaries.
*   `verify_logs.py`: Evaluates permanent row ingestion files to extract clean audit summaries.
# micron_project
