<?php
  error_reporting(0);

  class AdminPackage {

     public $password;
     public $leetness;

     function check_leetness() {
       if(md5($this->password) == '0e1337') echo '<pre> [+] Is it 1337? -> '.(assert('1337 == '.$this->leetness) ? 'Yes!' : 'Nope!').'</pre>';
     }

     function __construct($password, $leetness) {
       $this->password = $password; $this->leetness = $leetness;
     }
  }

  if(isset($_GET['a'])) {
    $admin_package = unserialize(base64_decode($_GET['a']));
    $admin_package->check_leetness();
  }
?>
