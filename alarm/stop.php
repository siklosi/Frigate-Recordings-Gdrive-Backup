<?php
$file = fopen("gbackup.ini", "w");
fwrite($file, "0");
fclose($file);
echo "Backup of recordings stoped.";
?>

