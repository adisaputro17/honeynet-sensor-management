    <!-- Sidebar -->
    <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

      <!-- Sidebar - Brand -->
      <a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.php">
        <div class="sidebar-brand-icon rotate-n-15">
          <i class="fab fa-docker"></i>
        </div>
        <div class="sidebar-brand-text mx-3">Admin</div>
      </a>

      <!-- Divider -->
      <hr class="sidebar-divider my-0">

      <!-- Nav Item - Dashboard -->
      <li class="nav-item">
        <a class="nav-link" href="index.php">
          <i class="fas fa-fw fa-tachometer-alt"></i>
          <span>Dashboard</span></a>
      </li>

      <!-- Divider -->
      <hr class="sidebar-divider">

      <!-- Heading -->
      <div class="sidebar-heading">
        Menu
      </div>

      <li class="nav-item">
        <a class="nav-link" href="agent.php">
          <i class="fas fa-fw fa-desktop"></i>
          <span>Agent</span></a>
      </li>

      <li class="nav-item">
        <a class="nav-link" href="sensor.php">
          <i class="fas fa-fw fa-sitemap"></i>
          <span>Sensor</span></a>
      </li>

      <!-- Divider -->
      <hr class="sidebar-divider d-none d-md-block">

      <!-- Heading -->
      <div class="sidebar-heading">
        Settings
      </div>

      <li class="nav-item">
        <a class="nav-link" href="change_password.php">
          <i class="fas fa-fw fa-cog"></i>
          <span>Change Password</span></a>
      </li>

      <li class="nav-item">
        <a class="nav-link" href="logout.php" onclick="return confirm('Are you sure?')">
          <i class="fas fa-fw fa-sign-out-alt"></i>
          <span>Logout</span></a>
      </li>

      <!-- Sidebar Toggler (Sidebar) -->
      <div class="text-center d-none d-md-inline">
        <button class="rounded-circle border-0" id="sidebarToggle"></button>
      </div>

    </ul>
    <!-- End of Sidebar -->