<?php

session_start();

if(!isset($_SESSION['admin'])){
    header('Location:login.php');
    exit;
}

include('koneksi.php');
?>

<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>Sensor</title>

  <!-- Custom fonts for this template -->
  <link href="vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i" rel="stylesheet">

  <!-- Custom styles for this template -->
  <link href="css/sb-admin-2.min.css" rel="stylesheet">

  <!-- Custom styles for this page -->
  <link href="vendor/datatables/dataTables.bootstrap4.min.css" rel="stylesheet">

</head>

<body id="page-top">

  <!-- Page Wrapper -->
  <div id="wrapper">

    <?php include('sidebar.php');?>

    <!-- Content Wrapper -->
    <div id="content-wrapper" class="d-flex flex-column">

      <!-- Main Content -->
      <div id="content">

        <!-- Topbar -->
        <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">

          <!-- Sidebar Toggle (Topbar) -->
          <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
            <i class="fa fa-bars"></i>
          </button>

          <!-- Topbar Search -->
          <form class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
            <div class="input-group">
              <input type="text" class="form-control bg-light border-0 small" placeholder="Search for..." aria-label="Search" aria-describedby="basic-addon2">
              <div class="input-group-append">
                <button class="btn btn-primary" type="button">
                  <i class="fas fa-search fa-sm"></i>
                </button>
              </div>
            </div>
          </form>

          <!-- Topbar Navbar -->
          <ul class="navbar-nav ml-auto">

            <!-- Nav Item - Search Dropdown (Visible Only XS) -->
            <li class="nav-item dropdown no-arrow d-sm-none">
              <a class="nav-link dropdown-toggle" href="#" id="searchDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fas fa-search fa-fw"></i>
              </a>
              <!-- Dropdown - Messages -->
              <div class="dropdown-menu dropdown-menu-right p-3 shadow animated--grow-in" aria-labelledby="searchDropdown">
                <form class="form-inline mr-auto w-100 navbar-search">
                  <div class="input-group">
                    <input type="text" class="form-control bg-light border-0 small" placeholder="Search for..." aria-label="Search" aria-describedby="basic-addon2">
                    <div class="input-group-append">
                      <button class="btn btn-primary" type="button">
                        <i class="fas fa-search fa-sm"></i>
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </li>

          </ul>

        </nav>
        <!-- End of Topbar -->

        <!-- Begin Page Content -->
        <div class="container-fluid">

          <!-- Page Heading -->
          <h1 class="h3 mb-4 text-gray-800">Sensor</h1>

          <?php
          $query = mysqli_query($koneksi, "select * from agent");
          if(mysqli_num_rows($query)>0){
            ?>

          <a href="#addSensor" data-toggle="modal" class="btn btn-success btn-icon-split mb-4">
            <span class="icon text-white-50">
              <i class="fas fa-plus"></i>
            </span>
            <span class="text">Add new Sensor</span>
          </a>

          <?php
          }else{
            ?>

          <a href="#addSensor" data-toggle="modal" class="btn btn-success btn-icon-split mb-4 disabled">
            <span class="icon text-white-50">
              <i class="fas fa-plus"></i>
            </span>
            <span class="text">Add new Sensor</span>
          </a>
          <?php
          }?>

          <!-- DataTales Example -->
          <div class="card shadow mb-4">
            <!-- <div class="card-header py-3">
              <h6 class="m-0 font-weight-bold text-primary">DataTables Example</h6>
            </div> -->
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Name</th>
                      <th>Agent</th>
                      <th>IP Address</th>
                      <th>Type</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>

                  	<?php
                  	$query = mysqli_query($koneksi, "select * from agent");
                  	$no = 1;
                  	while($row = mysqli_fetch_array($query)){
                  	?>

                  	<?php
                  	$url = 'http://' . $row['alamat'] . ':5555/containers/json?all=true';
                  	$ch = curl_init();
                  	curl_setopt($ch, CURLOPT_URL, $url);
                  	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
                  	$response = curl_exec($ch);
                  	curl_close($ch);
                  	$result = json_decode($response, true);
                  	?>

                    <tr>

                    <?php foreach ($result as $key => $member) : ?>
                      <td><?php echo $no++ ?></td>
                      <?php foreach ($member['Names'] as $key => $nama) : ?>
                        <td><?php $explodeNama = explode('/',$nama); echo $explodeNama[1] ?></td>
                      <?php endforeach; ?>

                  		<td><?php echo $row['nama'] ?></td>
                  		<td><?php echo $row['alamat'] ?></td>
                  		<td><?php $explodeImage = explode('/',$member['Image']); echo $explodeImage[1] ?></td>

                      <?php
                      if(strpos($member['State'], 'running') !== false){
                        echo '<td class="text-success">'.$member['Status'].'</td>';
                        echo '

                        <td>

                          <a href="stop_sensor.php?alamat='.$row['alamat'].'&nama='.$explodeNama[1].'" class="btn btn-warning btn-icon-split btn-sm">
                            <span class="icon text-white-50"><i class="fas fa-stop"></i></span>
                            <span class="text">Stop</span>
                          </a>

                          <a href="restart_sensor.php?alamat='.$row['alamat'].'&nama='.$explodeNama[1].'" class="btn btn-info btn-icon-split btn-sm">
                            <span class="icon text-white-50"><i class="fas fa-redo"></i></span>
                            <span class="text">Restart</span>
                          </a>

                          <a href="remove_sensor.php?alamat='.$row['alamat'].'&nama='.$explodeNama[1].'" class="btn btn-danger btn-icon-split btn-sm disabled">
                            <span class="icon text-white-50"><i class="fas fa-trash"></i></span>
                            <span class="text">Remove</span>
                          </a>
                        </td>

                        ';
                      }elseif(strpos($member['State'], 'exited') !== false){
                        $explodeStatus = explode(' ',$member['Status']);
                        $status = $explodeStatus[0] . ' ' . $explodeStatus[2] . ' ' . $explodeStatus[3] . ' ' . $explodeStatus[4];
                        echo '<td class="text-danger">'.$status.'</td>';
                        echo '

                        <td>
                          <a href="start_sensor.php?alamat='.$row['alamat'].'&nama='.$explodeNama[1].'" class="btn btn-success btn-icon-split btn-sm">
                            <span class="icon text-white-50"><i class="fas fa-play"></i></span>
                            <span class="text">Start</span>
                          </a>

                          <a href="restart_sensor.php?alamat='.$row['alamat'].'&nama='.$explodeNama[1].'" class="btn btn-info btn-icon-split btn-sm disabled">
                            <span class="icon text-white-50"><i class="fas fa-redo"></i></span>
                            <span class="text">Restart</span>
                          </a>

                          <a href="remove_sensor.php?alamat='.$row['alamat'].'&nama='.$explodeNama[1].'" class="btn btn-danger btn-icon-split btn-sm" onclick="return confirm(\'Are you sure?\')">
                            <span class="icon text-white-50"><i class="fas fa-trash"></i></span>
                            <span class="text">Remove</span>
                          </a>
                        </td>

                        ';
                      }else{
                        echo '<td>'.$member['Status'].'</td>';
                        echo '

                        <td>
                          <a href="start_sensor.php?alamat='.$row['alamat'].'&nama='.$explodeNama[1].'" class="btn btn-success btn-icon-split btn-sm">
                            <span class="icon text-white-50"><i class="fas fa-play"></i></span>
                            <span class="text">Start</span>
                          </a>

                          <a href="restart_sensor.php?alamat='.$row['alamat'].'&nama='.$explodeNama[1].'" class="btn btn-info btn-icon-split btn-sm disabled">
                            <span class="icon text-white-50"><i class="fas fa-redo"></i></span>
                            <span class="text">Restart</span>
                          </a>

                          <a href="remove_sensor.php?alamat='.$row['alamat'].'&nama='.$explodeNama[1].'" class="btn btn-danger btn-icon-split btn-sm" onclick="return confirm(\'Are you sure?\')">
                            <span class="icon text-white-50"><i class="fas fa-trash"></i></span>
                            <span class="text">Remove</span>
                          </a>
                        </td>

                        ';
                      }

                      ?>

                  	</tr>

                    <?php endforeach; ?>
                  	<?php
                  	}
                  	?>

                  </tbody>
                </table>
              </div>
            </div>
          </div>

        </div>
        <!-- /.container-fluid -->

      </div>
      <!-- End of Main Content -->

      <!-- Footer -->
      <footer class="sticky-footer bg-white">
        <div class="container my-auto">
          <div class="copyright text-center my-auto">
            <span>Copyright &copy; Implementation Docker Installer and Docker Management for Multi Honeynet</span>
          </div>
        </div>
      </footer>
      <!-- End of Footer -->

    </div>
    <!-- End of Content Wrapper -->

  </div>
  <!-- End of Page Wrapper -->

  <!-- Scroll to Top Button-->
  <a class="scroll-to-top rounded" href="#page-top">
    <i class="fas fa-angle-up"></i>
  </a>

  <!-- Add Agent Modal -->
  <div class="modal" id="addSensor">
    <div class="modal-dialog">
      <div class="modal-content">
      
        <!-- Modal Header -->
        <div class="modal-header">
          <h4 class="modal-title">Add New Sensor</h4>
          <button type="button" class="close" data-dismiss="modal">&times;</button>
        </div>
        
        <!-- Modal body -->
        <div class="modal-body">
          <form action="add_sensor.php" method="POST">
            <div class="form-group">
              <label>Name:</label>
              <input type="text" class="form-control" name="name" autocomplete="off" required="">
            </div>

            <div class="form-group">
              <label>Agent</label>
              <select class="form-control" name="agentOption">
                <?php
                $query = mysqli_query($koneksi, "select * from agent");
                while($row = mysqli_fetch_array($query)){
                  echo '<option>'.$row['nama'].'|'.$row['alamat'].'|'.'</option>';
                }
                ?>
              </select>
            </div>

            <div class="form-group">
              <label>Sensor</label>
              <select class="form-control" name="sensorOption">
                <option>cowrie</option>
                <option>dionaea</option>
                <option>glastopf</option>
              </select>
            </div>

            <button type="submit" class="btn btn-primary" name="btn_addAgent">Create Sensor</button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Bootstrap core JavaScript-->
  <script src="vendor/jquery/jquery.min.js"></script>
  <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

  <!-- Core plugin JavaScript-->
  <script src="vendor/jquery-easing/jquery.easing.min.js"></script>

  <!-- Custom scripts for all pages-->
  <script src="js/sb-admin-2.min.js"></script>

  <!-- Page level plugins -->
  <script src="vendor/datatables/jquery.dataTables.min.js"></script>
  <script src="vendor/datatables/dataTables.bootstrap4.min.js"></script>

  <!-- Page level custom scripts -->
  <script src="js/demo/datatables-demo.js"></script>

</body>

</html>