# Activate your virtual environment
call venv\Scripts\activate.bat

# Start the first Python script
python main.py

# Wait for 1 second
timeout /t 1 /nobreak

# Start the second Python script in a new terminal
start cmd /k python openobserve_exporter.py
