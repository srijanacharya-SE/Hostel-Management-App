-- DATABASE SETUP SCRIPT (HostelHub)
-- Copy and run this in your MySQL Terminal or Workbench

-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS HostelHub;
USE HostelHub;

-- 2. USERS (Login and Register)
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- 2.5. PROFILES (Owner Information)
CREATE TABLE IF NOT EXISTS profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE,
    admin_name VARCHAR(150),
    hostel_name VARCHAR(150),
    phone VARCHAR(50),
    email VARCHAR(200),
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

-- 3. ROOMS (For Room Management)
CREATE TABLE IF NOT EXISTS rooms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'available',
    type VARCHAR(50),
    capacity VARCHAR(50),
    occupied VARCHAR(50) DEFAULT '0 / 0',
    price VARCHAR(50),
    progress DOUBLE DEFAULT 0.0
);

-- 4. GUESTS (For Guest Directory and Payments)
-- Added bed_number column
CREATE TABLE IF NOT EXISTS guests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    initials VARCHAR(10),
    name VARCHAR(100) NOT NULL,
    room VARCHAR(50),
    bed_number VARCHAR(10),
    location VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    check_in VARCHAR(50),
    check_out VARCHAR(50),
    joining_date VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'Unpaid',
    paid_month VARCHAR(50) DEFAULT 'n/a'
);

-- 5. BOOKINGS
CREATE TABLE IF NOT EXISTS bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id VARCHAR(50),
    guest_name VARCHAR(100),
    room VARCHAR(50),
    check_in VARCHAR(50),
    check_out VARCHAR(50),
    guests_count VARCHAR(20),
    status VARCHAR(50)
);

-- 6. SETTINGS (For monthly reset logic)
CREATE TABLE IF NOT EXISTS settings (
    key_name VARCHAR(100) PRIMARY KEY,
    val VARCHAR(100)
);

-- 7. INITIAL CREDENTIALS (for testing)
-- You can log in with: admin / 1234
INSERT IGNORE INTO users (username, password) VALUES ('admin', '1234');
INSERT IGNORE INTO settings (key_name, val) VALUES ('last_reset_month', 'APRIL 2026');

-- 8. DUMMY DATA (Optional initial records)
INSERT IGNORE INTO rooms (name, type, price, capacity, status) VALUES ('101', 'Single', '$400', '1 beds', 'available'), ('102', 'Double', '$600', '2 beds', 'available');

-- VERIFY
SELECT 'Database Setup Updated Successfully!' AS Status;
