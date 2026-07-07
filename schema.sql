-- 1. Temporarily turn off foreign key constraints to clear old structures cleanly
PRAGMA foreign_keys = OFF;

-- 2. Drop dependent child tables first, then parent tables
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS test_scores;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS blogs;
DROP TABLE IF EXISTS analytics;

-- 3. Re-enable foreign key constraints for the new data structure
PRAGMA foreign_keys = ON;

-- Upgraded Users Table (Added roles, email, names, phone data)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone_code TEXT,
    phone_number TEXT,
    role TEXT NOT NULL DEFAULT 'student'
);

-- Applications Table
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    institution TEXT NOT NULL,
    program TEXT NOT NULL,
    scholarship_name TEXT NOT NULL,
    deadline DATE NOT NULL,
    status TEXT NOT NULL DEFAULT 'In Progress',
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Upgraded Test Scores Table
CREATE TABLE test_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    test_type TEXT NOT NULL,
    target_score REAL NOT NULL,
    current_score REAL,
    test_date DATE,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- NEW: Blogs / Scholarships Content Management
CREATE TABLE blogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    country TEXT,
    requirements TEXT,
    official_link TEXT,
    cover_image_path TEXT,
    content_html TEXT NOT NULL, -- Stores Rich Text (HTML formatting) from the editor
    opening_date DATE,
    deadline_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- NEW: Analytics Engine
CREATE TABLE analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_date DATE DEFAULT CURRENT_DATE,
    page_accessed TEXT NOT NULL,
    time_spent_seconds INTEGER DEFAULT 0,
    unique_visitor_id TEXT
);
