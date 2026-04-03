# WorkClaim
📌 WorkClaim – Facility Reservation System

WorkClaim is a role-based facility reservation system designed for managing shared resources such as classrooms, meeting rooms, and study areas within an institution.

The system allows users to create accounts, log in securely, and make reservations based on availability. Each reservation includes a time interval and is stored in a PostgreSQL database. The system ensures consistency and prevents conflicts using transactional operations.

A key feature of the project is its role-based priority mechanism. Users are categorized into roles such as student, instructor, and administrator. Higher-priority users can override existing reservations made by lower-priority users. When an override occurs, the affected user is notified through the system.

The backend is implemented in Python using a singleton database connection structure, ensuring efficient and centralized database access. Passwords are securely stored using hashing mechanisms. The system also includes periodic cleanup operations that remove expired reservations automatically.

The frontend is designed with PyQt, providing a simple and functional interface for interacting with the system.

🔧 Key Features
User registration and secure login (hashed passwords)
Role-Based Access Control (RBAC)
Facility filtering (capacity, type, features)
Reservation creation and cancellation
Role-based reservation override system
Notification mechanism for overridden reservations
Automatic cleanup of expired reservations
PostgreSQL-based persistent storage

🧠 Design Highlights
-Transaction-safe reservation handling 
-Conflict resolution using role hierarchy
-Modular database layer with reusable functions
-Scalable structure for adding new features

👥 Developers:
Emre Kaan Uzunöz - Backend(Python) And Database(PostgreSQL)
Zafer Burak Togur - Reservation Screen Connections(Python) & UI(PyQT)
Orhan Efe Yalçın - Reservation Screen Connections(Python) & UI(PyQT)
Mert Efe Karayılmaz - Main Menu Connections(Python) & UI(PyQT)
Hasan Yiğit Sarı - Login & Sign In Connections(Python) & UI(PyQt)

