<?php
$file = fopen("gbackup.ini", "w");
fwrite($file, "1");
fclose($file);
exec("nohup /usr/bin/python3 /var/www/html/alarm/gbackup.py > /dev/null 2>&1 &");
echo "Backup of recordings started.";
?>

