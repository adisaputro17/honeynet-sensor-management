<?php
include('koneksi.php');

echo '<link rel="stylesheet" href="css/sweetalert.css">';
echo '<script src="js/sweetalert.min.js"></script>';

$alamat = $_GET['alamat'];
$nama = $_GET['nama'];
$url = 'http://' . $alamat . ':5555/containers/' . $nama . '/start';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_exec($ch);

$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// echo $http_code;

if($http_code == 204){
	echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Sensor is started successfully',
	                type: 'success',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('sensor.php');
	      } ,2000); 
	      </script>";
}else{
	echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Type sensor is already running',
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

curl_close($ch);

?>