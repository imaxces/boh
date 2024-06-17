<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$servername = "127.0.0.1";
$username = "admin";
$password = "kali";
$dbname = "test_db";

// Creare connessione
$conn = new mysqli($servername, $username, $password, $dbname);

// Controllare connessione
if ($conn->connect_error) {
    die("Connessione fallita: " . $conn->connect_error);
}

if (isset($_GET['id'])) {
    $id = $_GET['id'];
    $sql = "SELECT * FROM users WHERE id = $id";

 } else {
    $sql = "SELECT * FROM users";
  } 
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            echo "ID: " . $row["id"]. " - Nome: " . $row["name"]. " - Email: " . $row["email"]. "<br>";
        }
    } else {
        echo "0 risultati";
    }
} else {
    echo "Nessun ID specificato";
}

$conn->close();
?>
