<?php
// Set CORS headers first (before any output)
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

require_once '../config/db.php';

$request_method = $_SERVER['REQUEST_METHOD'];
$action = isset($_GET['action']) ? $_GET['action'] : '';

// Health check endpoint for debugging
if ($action == 'health') {
    echo json_encode([
        'success' => true,
        'message' => 'API is running',
        'server_time' => date('Y-m-d H:i:s')
    ]);
    exit;
}

// Login verification
if ($action == 'login' && $request_method == 'POST') {
    $data = json_decode(file_get_contents("php://input"), true);
    $email = isset($data['email']) ? trim($data['email']) : '';
    $password = isset($data['password']) ? $data['password'] : '';
    
    // Validation
    if (empty($email) || empty($password)) {
        http_response_code(400);
        echo json_encode(['success' => false, 'error' => 'Email and password are required']);
        exit;
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode(['success' => false, 'error' => 'Invalid email format']);
        exit;
    }
    
    try {
        // Query admin table
        $query = "SELECT admin_id, admin_name, admin_email, access_level, admin_password FROM admin WHERE admin_email = ?";
        $stmt = $conn->prepare($query);
        
        if (!$stmt) {
            http_response_code(500);
            echo json_encode(['success' => false, 'error' => 'Database error: ' . $conn->error]);
            exit;
        }
        
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($result->num_rows > 0) {
            $admin = $result->fetch_assoc();
            
            // Verify password (plain text for now)
            if ($password === $admin['admin_password']) {
                http_response_code(200);
                echo json_encode([
                    'success' => true,
                    'message' => 'Login successful',
                    'admin_id' => $admin['admin_id'],
                    'admin_name' => $admin['admin_name'],
                    'admin_email' => $admin['admin_email'],
                    'access_level' => $admin['access_level']
                ]);
            } else {
                http_response_code(401);
                echo json_encode(['success' => false, 'error' => 'Invalid email or password']);
            }
        } else {
            http_response_code(401);
            echo json_encode(['success' => false, 'error' => 'Invalid email or password']);
        }
        
        $stmt->close();
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['success' => false, 'error' => 'Server error: ' . $e->getMessage()]);
    }
    exit;
}

// Get all parking slots
if ($action == 'get_slots') {
    $query = "SELECT * FROM parking_slots ORDER BY slot_id";
    $result = $conn->query($query);
    
    $slots = array();
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $slots[] = $row;
        }
    }
    
    echo json_encode(['success' => true, 'slots' => $slots]);
}

// Toggle slot status
else if ($action == 'toggle_slot' && $request_method == 'POST') {
    $data = json_decode(file_get_contents("php://input"), true);
    $slot_id = isset($data['slot_id']) ? intval($data['slot_id']) : 0;
    
    // Get current slot status
    $query = "SELECT slot_status, check_in_time FROM parking_slots WHERE slot_id = $slot_id";
    $result = $conn->query($query);
    
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $current_status = $row['slot_status'];
        
        // Toggle status
        if ($current_status == 'Available') {
            $new_status = 'Occupied';
            $check_in_time = date('Y-m-d H:i:s');
            $update_query = "UPDATE parking_slots SET slot_status = '$new_status', check_in_time = '$check_in_time' WHERE slot_id = $slot_id";
        } else {
            $new_status = 'Available';
            $check_out_time = date('Y-m-d H:i:s');
            $update_query = "UPDATE parking_slots SET slot_status = '$new_status', check_out_time = '$check_out_time' WHERE slot_id = $slot_id";
        }
        
        if ($conn->query($update_query)) {
            // Log the action
            $log_query = "INSERT INTO admin_logs (admin_id, action, slot_id, description) VALUES (1, 'toggle_slot', $slot_id, 'Status changed to $new_status')";
            $conn->query($log_query);
            
            echo json_encode(['success' => true, 'new_status' => $new_status, 'timestamp' => date('Y-m-d H:i')]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Failed to toggle slot']);
        }
    } else {
        echo json_encode(['success' => false, 'error' => 'Slot not found']);
    }
}

// Get parking slots summary
else if ($action == 'get_summary') {
    $query = "SELECT 
                (SELECT COUNT(*) FROM parking_slots WHERE slot_status = 'Available') as available,
                (SELECT COUNT(*) FROM parking_slots WHERE slot_status = 'Occupied') as occupied,
                (SELECT COUNT(*) FROM parking_slots) as total";
    
    $result = $conn->query($query);
    $summary = $result->fetch_assoc();
    
    $summary['occupancy_percent'] = $summary['total'] > 0 ? round(($summary['occupied'] / $summary['total']) * 100) : 0;
    
    echo json_encode(['success' => true, 'summary' => $summary]);
}

// Reset all slots to available
else if ($action == 'reset_slots' && $request_method == 'POST') {
    $update_query = "UPDATE parking_slots SET slot_status = 'Available', check_in_time = NULL, check_out_time = NULL";
    
    if ($conn->query($update_query)) {
        // Log the action
        $log_query = "INSERT INTO admin_logs (admin_id, action, description) VALUES (1, 'reset_slots', 'All slots reset to available')";
        $conn->query($log_query);
        
        echo json_encode(['success' => true, 'message' => 'All slots reset']);
    } else {
        echo json_encode(['success' => false, 'error' => 'Failed to reset slots']);
    }
}

// Get parking history for analytics
else if ($action == 'get_history') {
    $query = "SELECT * FROM parking_history ORDER BY history_id DESC LIMIT 100";
    $result = $conn->query($query);
    
    $history = array();
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $history[] = $row;
        }
    }
    
    echo json_encode(['success' => true, 'history' => $history]);
}

// Get parking rates
else if ($action == 'get_rates') {
    $query = "SELECT * FROM parking_rates WHERE status = 'active'";
    $result = $conn->query($query);
    
    $rates = array();
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $rates[] = $row;
        }
    }
    
    echo json_encode(['success' => true, 'rates' => $rates]);
}

// Get admin information
else if ($action == 'get_admin') {
    $query = "SELECT admin_id, admin_name, admin_email, access_level, status FROM admin WHERE admin_id = 1";
    $result = $conn->query($query);
    
    if ($result->num_rows > 0) {
        $admin = $result->fetch_assoc();
        echo json_encode(['success' => true, 'admin' => $admin]);
    } else {
        echo json_encode(['success' => false, 'error' => 'Admin not found']);
    }
}

else {
    echo json_encode(['error' => 'Invalid action']);
}

$conn->close();
?>
