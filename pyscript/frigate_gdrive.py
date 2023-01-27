import requests
s = requests.Session()
start_url="http://10.1.1.2:81/alarm/start.php"
stop_url="http://10.1.1.2:81/alarm/stop.php"
@state_trigger("input_boolean.gdrive_frigate")
def gdrive_backup_toggle():
    if input_boolean.gdrive_frigate=="on":
        response = task.executor(s.get, start_url, timeout=10,  verify=False)
    if input_boolean.gdrive_frigate=="off":
        response = task.executor(s.get, stop_url, timeout=10,  verify=False)