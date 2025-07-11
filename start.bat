@echo off
REM Install all required Python dependencies for the airline dashboard project

REM Use the user's default python installation
python -m pip install --upgrade pip
python -m pip install pandas numpy plotly dash dash-bootstrap-components selenium openpyxl scipy

REM Optional: Remind user to install ChromeDriver if exporting dashboard as HTML

echo.
echo All dependencies installed. If you want to export the dashboard as HTML, make sure ChromeDriver is installed and in your PATH.
pause