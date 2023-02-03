title Weather Station Web Server (DO NOT CLOSE THIS WINDOW)
echo Starting Web Server...
start /B python3 .\web_server.py
start /B .\ngrok http --scheme=http --region=us --hostname=weatherstation.ngrok.io 8000