USE HostelHub;

TRUNCATE TABLE rooms;
INSERT IGNORE INTO rooms (name, status, type, capacity, occupied, price, progress) VALUES 
('101', 'occupied', 'Dormitory', '8 beds', '6 / 8', '$15', 0.75), 
('102', 'occupied', 'Dormitory', '8 beds', '8 / 8', '$15', 1.0), 
('103', 'available', 'Dormitory', '6 beds', '0 / 6', '$18', 0.0);

TRUNCATE TABLE guests;
INSERT IGNORE INTO guests (initials, name, room, location, email, phone, check_in, check_out, joining_date, payment_status, paid_month) VALUES 
('JS', 'John Smith', '101', 'USA', 'john.smith@email.com', '+1-234-567-8901', '2026-02-25', '2026-03-02', '2026-04-01', 'Paid', 'April 2026'), 
('EW', 'Emma Wilson', '201', 'UK', 'emma.w@email.com', '+44-20-1234-5678', '2026-02-27', '2026-03-01', '2026-04-01', 'Paid', 'April 2026'), 
('MC', 'Michael Chen', '302', 'China', 'm.chen@email.com', '+86-138-0013-8000', '2026-02-26', '2026-03-05', '2026-04-01', 'Paid', 'April 2026');

TRUNCATE TABLE bookings;
INSERT IGNORE INTO bookings (booking_id, guest_name, room, check_in, check_out, guests_count, status) VALUES 
('#1', 'John Smith', '101', '📅 2026-02-25', '📅 2026-03-02', '1', 'checked-in'), 
('#2', 'Emma Wilson', '201', '📅 2026-02-27', '📅 2026-03-01', '2', 'checked-in'), 
('#3', 'Michael Chen', '302', '📅 2026-02-26', '📅 2026-03-05', '3', 'checked-in');
