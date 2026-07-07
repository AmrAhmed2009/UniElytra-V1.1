UniElytra
Video Demo: (https://youtu.be/8p69v4lkTRg?si=gTmaBBsFXIHy3KLG)
Description:
UniElytra is a centralized, data-driven full-stack web application designed to act as a digital flight deck for global scholars navigating the highly competitive landscape of international university admissions and fully funded undergraduate scholarship tracks. Ambitious students applying for high-stakes programs—such as the Stipendium Hungaricum or tracks at Hamad Bin Khalifa University—frequently face a disjointed ecosystem of shifting deadlines, multi-tiered degree classifications, and critical standardized testing requirements. Managing these elements across multiple spreadsheets or notebooks quickly leads to administrative friction. UniElytra unifies these isolated workflows into a web platform engineered around real-world UI/UX principles, secure session management, and persistent relational data storage.

The application’s core architecture focuses heavily on human-centered design. Rather than greeting a new user with barren, unstyled tables, UniElytra implements dynamic dashboard empty states that display professional placeholder graphics and actionable instructions. The system isolates data into two pipelines: the institutional application tracking matrix and the propulsion benchmarks center. The applications engine manages complex timelines and multi-cycle dates, allowing users to track university options across Bachelor, Master, or PhD tiers. For specialized international funding bodies, the platform features dynamic text input validation that updates in real time on the frontend. Meanwhile, the testing dashboard isolates tracking indicators for exams like the SAT and IELTS Academic, allowing students to visually audit the margins between their current baselines and their dream scores.

File Inventory and Structural Breakdown:
app.py
This file serves as the primary controller and logical backbone of the entire application. Written in Python utilizing the Flask framework, it manages request routing, enforces security middleware to protect user-restricted views, handles session clearings, and communicates directly with the database. It contains explicit logic to process both incoming GET and POST payloads, validate credential sets securely, pass context arrays to the Jinja2 template renderer, and handle error catching gracefully to prevent server crashes.

schema.sql
The blueprint for the database architecture. This file contains the exact structural relational commands required to construct the tables within the database engine. It builds a users table featuring unique constraints and hashed credential storage, an applications tracking table linked by secondary user foreign keys, and a tests configuration table to store exam variants, user goals, and dates cleanly.

tracker.db
The production-ready relational SQLite database instance. This file preserves structural states persistently. It handles server-side inserts, updates, and deletes triggered by user input forms from the active web frontend, ensuring that user metrics remain securely isolated and permanent over time.

templates/layout.html
The universal master template layout that acts as the global wrapper framework for the front end. Built using modern semantic HTML5 and customized Bootstrap 5 utilities, this file houses the application’s signature deep-purple styling theme overrides, global responsive navbar configurations, flash message notifications blocks, and the official founder manifesto system footer. It uses Jinja2 block injection tags ({% block main %}) to efficiently inherit visual properties down to individual page views.

templates/index.html
The main user hub and operational dashboard screen. This file uses Jinja2 structural conditionals to read database output lists. If the current user has zero records on file, it changes layout states dynamically to display the custom system onboarding empty-state panel. If rows exist, it organizes data into highly scannable tracking metrics, table logs, and performance card vectors.

templates/add_application.html
The formal interface used to log target academic institutions. This file contains input validations for tracking variables like deadline timing, program types, and funding structures. Crucially, it houses embedded client-side JavaScript loops that hook directly into the program tier drop-down box; if a scholar selects the option marked "Other," the script manipulates the DOM to reveal hidden text containers immediately.

templates/add_test.html
The testing matrix registration interface. It features specialized numeric forms and selection toggles dedicated to recording standardized milestones like the SAT, Digital SAT, and IELTS Academic. It restricts inputs to realistic bounds and coordinates date logging to evaluate performance trajectory.

templates/login.html
A secure entry-point configuration page. It utilizes optimized Bootstrap row layouts and card boundaries to focus user attention entirely on the access fields. It communicates over secure POST channels to pass input variables directly into the server authentication routine.

templates/register.html
The account provisioning template. It matches the signature visual theme of the application and requires dual matching password confirmations, parsing inputs defensively on the client side before allowing user configuration files to be processed by the backend.
