#!/bin/bash

# Initialize the local database schema if it has not been deployed yet
python3 setup_factory_db.py

# Launch the continuous production data pipeline using terminal stream piping
python3 tool_simulator.py | python3 fdc_processor.py
