<?php
include('koneksi.php');
session_start();

echo '<link rel="stylesheet" href="css/sweetalert.css">';
echo '<script src="js/sweetalert.min.js"></script>';

if(isset($_SESSION['admin'])){
    header('Location:index.php');
    exit;
}

?>
<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>Login</title>

  <!-- Custom fonts for this template-->
  <link href="vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i" rel="stylesheet">

  <!-- Custom styles for this template-->
  <link href="css/sb-admin-2.min.css" rel="stylesheet">

</head>

<body class="bg-gradient-primary">

  <div class="container">

    <!-- Outer Row -->
    <div class="row justify-content-center">

      <div class="col-md-6">

        <div class="card o-hidden border-0 shadow-lg my-5">
          <div class="card-body p-0">

            <div class="p-5">
                  <div class="text-center">
                    <h1 class="h4 text-gray-900 mb-4">Login</h1>
                  </div>
                  <form action="" method="POST">
                    <div class="form-group">
                      <input type="text" class="form-control" placeholder="Username" name="username" autocomplete="off" required>
                    </div>
                    <div class="form-group">
                      <input type="password" class="form-control" placeholder="Password" name="password" autocomplete="off" required>
                    </div>
                    <button class="btn btn-primary btn-user btn-block" name="login" type="submit">Login</button>
                  </form>
                </div>

          </div>
        </div>

      </div>

    </div>

  </div>

<?php
if(isset($_POST['login'])){
  $username = $_POST['username'];
  $password = $_POST['password'];

  $data = mysqli_query($koneksi,"select * from admin where username='$username' and password='$password'");
  $cek = mysqli_num_rows($data);

  if($cek == 1){
    $_SESSION['admin'] = $username;

    echo "<script type='text/javascript'>
        setTimeout(function () { 
          swal({
                  title: 'Login is successfully',
                  type: 'success',
                  timer: 2000,
                  showConfirmButton: true
              });   
        },10);  
        window.setTimeout(function(){ 
          window.location.replace('index.php');
        } ,2000); 
        </script>";

  }else{

    echo "<script type='text/javascript'>
        setTimeout(function () { 
          swal({
                  title: 'Login failed',
                  text: 'Invalid Username or Password',
                  type: 'error',
                  timer: 2000,
                  showConfirmButton: true
              });   
        },10);  
        window.setTimeout(function(){ 
          window.location.replace('login.php');
        } ,2000); 
        </script>";

  }
}
?>

  <!-- Bootstrap core JavaScript-->
  <script src="vendor/jquery/jquery.min.js"></script>
  <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

  <!-- Core plugin JavaScript-->
  <script src="vendor/jquery-easing/jquery.easing.min.js"></script>

  <!-- Custom scripts for all pages-->
  <script src="js/sb-admin-2.min.js"></script>

</body>

</html>
