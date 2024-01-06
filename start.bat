# Activate your virtual environment
call venv\Scripts\activate.bat
# Start the second Python script in a new terminal
start cmd /k pythonw.exe openobserve_exporter.py
# Start the first Python script in the current terminal
pythonw.exe main.py
```
