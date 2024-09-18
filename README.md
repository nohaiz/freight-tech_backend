# *Freight-Tech*
 
 ## DATE: 12-9-2024
 
 ## [Project Plan](https://trello.com/b/FU9oY9v0/freight-tech)
 
 ### Project Team
 
 1. Sayed Ahmed Alali
 2. Nohaiz Kaiser
 3. Qasim Alhamad
 
 ## Description
 
 *Freight-Tech* is a logistics management system designed to streamline delivery tracking and management. It provides functionalities for users such as admins, shippers, and drivers to manage deliveries efficiently.
 
 ## Technologies Used
 
 - *Flask*: Micro web framework for handling backend logic and API endpoints.
 - *PostgreSQL*: Relational database for storing user and delivery information.
 - *SQLAlchemy*: ORM (Object-Relational Mapping) tool for database interactions.
 - *Flask-JWT*: For handling authentication and authorization.
 
 ### Development Tools:
 
 - *Flask-Migrate*: For database migrations and schema changes.
 - *Postman*: For testing API endpoints and viewing responses.
 - *React Developer Tools*: For debugging React applications.
 
 ## How It Works
 
 1. *User Management:*
 
    - *Create*: Admins can create new user accounts with specified roles.
    - *Read*: View details of existing user accounts.
    - *Update*: Modify user account details and roles.
    - *Delete*: Remove user accounts from the system.
    - *Role-based Access Control*: Different functionalities available based on user roles (Admin, Shipper, Driver).
 
 2. *Delivery Management:*
 
    - *Create*: Add new delivery entries with necessary details.
    - *Read*: View delivery details and status.
    - *Update*: Modify delivery information, including status and assigned drivers.
    - *Delete*: Remove delivery records from the system.
    - *Track Status*: Monitor delivery status (Pending, Complete, InProgress).
    - *Assign Drivers*: Assign available drivers to specific deliveries.
    - *Capture Details*: Record details like payment amount, vehicle type, dimensions, weight value, and delivery time.
 
 3. *Role Management:*
    - *CRUD Operations for Roles*: Create, read, update, and delete roles.
    - *Associate Users with Roles*: Link users to specific roles, defining their access levels.
 
 ## Future Updates
 
 - [ ] Implement a notification system for delivery updates and status changes.
 - [ ] Enhance validation processes for input data.
 - [ ] Improve UI/UX design for a more intuitive user experience.
 
 ## Useful Links
 
 - [Markdown Cheat-Sheet](https://www.markdownguide.org/cheat-sheet/)
 - [React Documentation](https://reactjs.org/docs/getting-started.html)
 - [Flask Documentation](https://flask.palletsprojects.com/en/2.2.x/)
 - [PostgreSQL Documentation](https://www.postgresql.org/docs/)
 - [Stack Overflow](https://stackoverflow.com/)