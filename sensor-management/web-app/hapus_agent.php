<?php
include('koneksi.php');

echo '<link rel="stylesheet" href="css/sweetalert.css">';
echo '<script src="js/sweetalert.min.js"></script>';

$id_agent = $_GET['id_agent'];
$sql_hapus = "DELETE FROM agent WHERE id_agent=" . $id_agent;
$hapus = mysqli_query($koneksi, $sql_hapus) or die(mysqli_error($koneksi));

if($hapus){
	echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Agent is removed successfully',
	                type: 'success',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('agent.php');
	      } ,2000); 
	      </script>";
}else{
	echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Agent is not found',
	                type: 'error',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('agent.php');
	      } ,2000); 
	      </script>";
}

?>