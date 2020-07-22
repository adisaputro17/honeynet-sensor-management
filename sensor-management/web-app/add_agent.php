<?php
include('koneksi.php');

echo '<link rel="stylesheet" href="css/sweetalert.css">';
echo '<script src="js/sweetalert.min.js"></script>';

$nama = $_POST['name'];
$alamat = $_POST['address'];
$url = 'http://' . $alamat . ':5555/containers/json?all=true';

// Create a curl handle to a non-existing location
$ch = curl_init($url);

// Execute
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 1); //timeout in seconds
curl_exec($ch);

// Check if any error occurred
if(curl_errno($ch))
{
    echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Could not add Agent',
	                type: 'error',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('agent.php');
	      } ,2000); 
	      </script>";
}else{

	$sql_cek = mysqli_query($koneksi,"SELECT * FROM agent where nama='$nama' or alamat='$alamat'");
	if(mysqli_num_rows($sql_cek) > 0 ){
		echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Agent is ready',
	                type: 'error',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('agent.php');
	      } ,2000); 
	      </script>";
	  }else{
	  	$sql_tambah = "INSERT INTO agent (nama, alamat) VALUES ('$nama','$alamat')";
	  	$tambah = mysqli_query($koneksi, $sql_tambah) or die(mysqli_error($koneksi));

	  	echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Agent is added successfully',
	                type: 'success',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('agent.php');
	      } ,2000); 
	      </script>";
	  }
}

// Close handle
curl_close($ch);

?>