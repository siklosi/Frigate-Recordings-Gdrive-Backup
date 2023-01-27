# Frigate-Recordings-Gdrive-Backup
Scripts that upload Frigate recordings to google drive

Idea behind this is that if thief's take server where frigate is recording than there is no use of cameras and...

I have input boolean in Home Assistant that is swithed on by automation on alarm triggered and turned off when alarm changes state back to disarmed.

pyscript [frigate_gdrive.py](https://github.com/siklosi/Frigate-Recordings-Gdrive-Backup/blob/main/pyscript/frigate_gdrive.py) when switch is turned on calls [start.php](https://github.com/siklosi/Frigate-Recordings-Gdrive-Backup/blob/main/alarm/start.php) 
and when switch is turned off calls [stop.php](https://github.com/siklosi/Frigate-Recordings-Gdrive-Backup/blob/main/alarm/stop.php). start.php writes "1" to gbackup.ini and calls [gbackup.py]https://github.com/siklosi/Frigate-Recordings-Gdrive-Backup/blob/main/alarm/gbackup.py that uploads frigate video clips not older then 10 hours (can be changed) and goes into loop while 1 is in gbackup.ini and checks every 10 seconds if there is new video clip and uploads it to gdrive.
stop.php script writes "0" to gbackup.ini cousing gbackup.py to exit script.
