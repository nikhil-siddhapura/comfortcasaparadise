-- ============================================================
-- RESORT MANAGEMENT SYSTEM — MySQL Database Schema
-- Run this file FIRST before starting the backend
-- Command: mysql -u root -p < resort_db.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS resort_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE resort_db;

-- ── Users ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    password      VARCHAR(255) NOT NULL,
    phone         VARCHAR(20),
    bio           TEXT,
    profile_image VARCHAR(255),
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Categories ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS categories (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    description TEXT,
    price       DECIMAL(10,2) NOT NULL,
    image       VARCHAR(255),
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Products ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS products (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    category_id     INT NOT NULL,
    name            VARCHAR(150) NOT NULL,
    description     TEXT,
    price           DECIMAL(10,2) NOT NULL,
    total_rooms     INT DEFAULT 1,
    available_rooms INT DEFAULT 1,
    image           VARCHAR(255),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- ── Bookings ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS bookings (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT NOT NULL,
    product_id    INT NOT NULL,
    check_in      DATE NOT NULL,
    check_out     DATE NOT NULL,
    adults        INT NOT NULL DEFAULT 1,
    children      INT DEFAULT 0,
    total_price   DECIMAL(10,2),
    status        ENUM('pending','approved','rejected') DEFAULT 'pending',
    admin_message TEXT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_booking_user    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE CASCADE,
    CONSTRAINT fk_booking_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- ── Feedback ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS feedback (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL,
    booking_id INT NOT NULL,
    rating     INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment    TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_feedback_user    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE CASCADE,
    CONSTRAINT fk_feedback_booking FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
);

-- ── Contacts ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS contacts (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT DEFAULT NULL,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL,
    subject     VARCHAR(200),
    message     TEXT NOT NULL,
    admin_reply TEXT,
    is_read     BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_contact_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- ── Services ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS services (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    description TEXT,
    price       DECIMAL(10,2) NOT NULL,
    image       VARCHAR(255),
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Booking ↔ Services (Many-to-Many) ────────────────────────
CREATE TABLE IF NOT EXISTS booking_services (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    service_id INT NOT NULL,
    CONSTRAINT fk_bs_booking FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    CONSTRAINT fk_bs_service FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
);

-- ── Password Resets ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS password_resets (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    email      VARCHAR(100) NOT NULL,
    token      VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used       BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SAMPLE DATA
-- ============================================================

INSERT INTO categories (name, description, price) VALUES
('Deluxe Room',     'Spacious rooms with stunning sea view and king-size bed',    4999.00),
('Suite',           'Luxury suites with private jacuzzi and lounge area',         12999.00),
('Banquet Hall',    'Grand hall for weddings, events and corporate functions',    49999.00),
('Conference Room', 'Fully equipped boardroom with AV system',                    9999.00),
('Villa',           'Private villa with pool, garden and chef on request',        24999.00);

INSERT INTO products (category_id, name, description, price, total_rooms, available_rooms) VALUES
(1, 'Ocean View Deluxe',       'King bed, ocean view, 24hr room service, free WiFi',    5499.00, 10, 8),
(1, 'Garden Deluxe Room',      'Queen bed, garden view, private balcony',               4999.00,  8, 7),
(2, 'Royal Presidential Suite','Jacuzzi, butler service, panoramic views, 2 bedrooms', 15999.00,  3, 3),
(2, 'Honeymoon Suite',         'Rose decor, private terrace, champagne on arrival',    13499.00,  2, 2),
(3, 'Grand Ballroom',          '500-seat hall with stage, AV system, catering',        55000.00,  1, 1),
(4, 'Executive Boardroom',     '20 seats, projector, video conferencing setup',        11999.00,  2, 2),
(5, 'Garden Pool Villa',       'Private pool, 3 BHK villa, chef on request',           27999.00,  5, 4);

INSERT INTO services (name, description, price) VALUES
('Spa & Wellness',     'Full body relaxation and rejuvenation spa package',   2999.00),
('Airport Transfer',   'Comfortable pickup and drop from nearest airport',    1499.00),
('Candlelight Dinner', 'Private rooftop dinner for two with live music',      3999.00),
('Gym Access',         'Full-day access to fitness center and equipment',      299.00),
('Room Service',       '24/7 in-room dining with premium menu',               499.00);
