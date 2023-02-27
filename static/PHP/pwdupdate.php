<?php
// Start session and check if user is logged in
session_start();
if (!isset($_SESSION['user_id'])) {
	header("Location: login.php");
	exit();
}

// Check if form was submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	// Get form data
	$old_password = $_POST['old_password'];
	$new_password = $_POST['new_password'];
	$confirm_password = $_POST['confirm_password'];

	// Check if new password and confirm password match
	if ($new_password !== $confirm_password) {
		echo "Error: New password and confirm password do not match.";
		exit();
	}

	// TODO: Validate new password strength and complexity

	// TODO: Verify old password

	// TODO: Update password in database

	// Redirect to success page
	header("Location: password_updated.php");
	exit();
}
?>
