<?php
header('Content-Type: application/json'); // Set response type to JSON
header('Access-Control-Allow-Origin: *'); // Allow requests from any origin (for testing, be specific in production)
header('Access-Control-Allow-Methods: POST, OPTIONS'); // Allow POST and OPTIONS methods
header('Access-Control-Allow-Headers: Content-Type'); // Allow Content-Type header

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') { // Handle OPTIONS preflight requests
    http_response_code(200); // Respond with OK for preflight
    exit();
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $target_url = 'http://localhost:5000/classify'; // Your Python Flask server URL

    // Get the JSON data from the incoming request
    $request_data = file_get_contents('php://input');

    // Initialize CURL
    $ch = curl_init($target_url);

    // Set CURL options
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // Return response as string
    curl_setopt($ch, CURLOPT_POST, true);        // Set as POST request
    curl_setopt($ch, CURLOPT_POSTFIELDS, $request_data); // Send the JSON data
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json')); // Set Content-Type header for POST

    // Execute CURL request
    $response_json = curl_exec($ch);

    // Check for CURL errors
    if (curl_errno($ch)) {
        http_response_code(500); // Internal Server Error on proxy side
        echo json_encode(['error' => 'CURL error: ' . curl_error($ch)]);
    } else {
        $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($httpcode == 200) {
            echo $response_json; // Send the Python server's response back to the client
        } else {
            http_response_code($httpcode); // Forward the HTTP status code from Python server
            echo $response_json;       // Also forward the body in case of error responses
        }
    }

    curl_close($ch);
} else {
    http_response_code(400); // Bad Request if not POST
    echo json_encode(['error' => 'Only POST requests are allowed']);
}
?>