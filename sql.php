<?php
$servername = "localhost";
$username = "root";
$password = "la_tua_password_di_mysql";
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
