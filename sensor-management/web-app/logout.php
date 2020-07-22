<?php

echo '<link rel="stylesheet" href="css/sweetalert.css">';
echo '<script src="js/sweetalert.min.js"></script>';

session_start();
session_destroy();

echo "<script type='text/javascript'>
	      setTimeout(function () { 
	        swal({
	                title: 'Logout is successfully',
	                type: 'success',
	                timer: 2000,
	                showConfirmButton: true
	            });   
	      },10);  
	      window.setTimeout(function(){ 
	        window.location.replace('login.php');
	      } ,2000); 
	      </script>";
?>