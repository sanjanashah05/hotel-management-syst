CREATE TABLE rooms (
room_id INT AUTO_INCREMENT PRIMARY KEY,
type VARCHAR(50),
price DECIMAL(10, 2),
status ENUM(&#39;available&#39;, &#39;booked&#39;, &#39;maintenance&#39;) DEFAULT &#39;available&#39;
);

CREATE TABLE customers (
customer_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100),
phone VARCHAR(15)
);

CREATE TABLE reservations (
reservation_id INT AUTO_INCREMENT PRIMARY KEY,
customer_id INT,
room_id INT,
check_in DATE,
check_out DATE,
status ENUM(&#39;active&#39;, &#39;completed&#39;, &#39;cancelled&#39;) DEFAULT &#39;active&#39;,
FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE TABLE payments (
payment_id INT AUTO_INCREMENT PRIMARY KEY,
reservation_id INT,
amount DECIMAL(10, 2),
payment_date DATE,
payment_method ENUM(&#39;cash&#39;, &#39;credit card&#39;, &#39;online&#39;),
FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id)
);

CREATE TABLE staff (
staff_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
position VARCHAR(50),
salary DECIMAL(10, 2)
);
--------------------------------------VIE3WS------------------------------------------------------------------------
CREATE VIEW available_rooms AS
SELECT * FROM rooms WHERE status = &#39;available&#39;;

CREATE VIEW active_reservations AS
SELECT * FROM reservations WHERE status = &#39;active&#39;;

--------------------------------------PRoCEDURES------------------------------------------------------------------------

DELIMITER //

CREATE PROCEDURE set_room_status(IN room INT, IN new_status ENUM(&#39;available&#39;, &#39;booked&#39;, &#39;maintenance&#39;))
BEGIN
UPDATE rooms SET status = new_status WHERE room_id = room;
END //

CREATE PROCEDURE delete_reservation(IN reservation INT)
BEGIN
-- Set the room as available
UPDATE rooms SET status = &#39;available&#39;
WHERE room_id = (SELECT room_id FROM reservations WHERE reservation_id = reservation);

-- Delete the reservation
DELETE FROM reservations WHERE reservation_id = reservation;
END //

DELIMITER ;
--------------------------------------TRIGGERS------------------------------------------------------------------------
DELIMITER //

CREATE TRIGGER update_room_on_booking
AFTER INSERT ON reservations

FOR EACH ROW
BEGIN
UPDATE rooms SET status = &#39;booked&#39; WHERE room_id = NEW.room_id;
END //

CREATE TRIGGER update_room_on_cancellation
AFTER DELETE ON reservations
FOR EACH ROW
BEGIN
UPDATE rooms SET status = &#39;available&#39; WHERE room_id = OLD.room_id;
END //

DELIMITER ;