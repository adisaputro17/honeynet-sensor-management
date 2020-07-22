<?php
include('koneksi.php');

echo '<link rel="stylesheet" href="css/sweetalert.css">';
echo '<script src="js/sweetalert.min.js"></script>';

$nama = str_replace(" ","_",$_POST['name']);
$agentOption = explode('|',$_POST['agentOption']);
$sensorOption = $_POST['sensorOption'];
$cek = 0;

$urlCek = 'http://' . $agentOption[1] . ':5555/containers/json?all=true';
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $urlCek);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$response = curl_exec($ch);
curl_close($ch);
$result = json_decode($response, true);

foreach ($result as $key => $member) :
	if(strpos($member['Image'], $sensorOption) !== false){
		$cek = 1;
	}
endforeach;

$fileCowrie = file_get_contents("cowrie.json");
$fileDionaea = file_get_contents("dionaea.json");
$fileGlastopf = file_get_contents("glastopf.json");

$urlAdd = 'http://' . $agentOption[1] . ':5555/containers/create?name=' .$nama;

function curl($url, $data){
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
	curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
	curl_setopt( $ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_exec($ch);
	$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	curl_close($ch);
	return $http_code;
}

if($cek == 0){

	if($sensorOption == 'cowrie'){
		$resultAdd = curl($urlAdd,$fileCowrie);
		if($resultAdd == 201){
			echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Sensor is added successfully',
	                type: 'success',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('sensor.php');
	      } ,2000); 
	      </script>";
		}
	}

	if($sensorOption == 'dionaea'){
		$resultAdd = curl($urlAdd,$fileDionaea);
		if($resultAdd == 201){
			echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Sensor is added successfully',
	                type: 'success',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('sensor.php');
	      } ,2000); 
	      </script>";
		}
	}

	if($sensorOption == 'glastopf'){
		$resultAdd = curl($urlAdd,$fileGlastopf);
		if($resultAdd == 201){
			echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Sensor is added successfully',
	                type: 'success',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('sensor.php');
	      } ,2000); 
	      </script>";
		}
	}

}else{
	echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Sensor is found',
	                type: 'error',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('sensor.php');
	      } ,2000); 
	      </script>";
}



?>