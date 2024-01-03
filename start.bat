# Activate your virtual environment
call venv\Scripts\activate.bat
# Start the second Python script in a new terminal
start cmd /k pythonw.exe openobserve_exporter.py

# Start the first Python script
python main.py
