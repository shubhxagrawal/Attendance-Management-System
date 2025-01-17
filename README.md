# Attendance Management System

This project is an **Attendance Management System** built using **Flask**, a Python web framework, and **SQLite** as the database. The system allows professors to manage student attendance for different divisions, view reports, and perform CRUD operations on student data.

## Technology Used

- **Frontend**:
  - HTML
  - CSS
  - Bootstrap 5 for responsive design and styling

- **Backend**:
  - Python
  - Flask web framework
  - SQLite for database management

- **Libraries**:
  - `Flask`: A micro web framework for Python.
  - `Flask-SQLAlchemy`: An ORM for working with SQLite.
  - `Jinja2`: Templating engine used in Flask for rendering HTML.
  - `Bootstrap`: A front-end framework for responsive web design.

## Features

- **Professor Login**: Professors can log in to the system to manage attendance.
- **Student Management**: Professors can add, view, and remove students from the system.
- **Attendance Marking**: Professors can mark attendance for students for a specific date and division.
- **Attendance Reports**: Professors can view monthly attendance reports for each student.
- **Responsive Design**: The application is mobile-friendly and looks good on all screen sizes.

## Steps to Run the Project

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/your-username/attendance-system.git
cd attendance-system
```

### 2. Set Up the Virtual Environment

It's recommended to use a virtual environment to manage dependencies. If you don't have `virtualenv` installed, you can install it using `pip`:

```bash
pip install virtualenv
```

Create a virtual environment:

```bash
virtualenv venv
```

Activate the virtual environment:

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

- On macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

The project uses SQLite, and the database will be automatically created when you run the app. However, you can manually create the database tables by running the following command:

```bash
python
>>> from app import db
>>> db.create_all()
```

This will create the necessary tables in the SQLite database (`attendance.db`).

### 5. Run the Application

To start the Flask development server, run the following command:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000/` in your browser.

### 6. Access the Application

- **Login**: Use the default professor credentials to log in:
  - Username: `root`
  - Password: `root`

- **Dashboard**: After logging in, you will be redirected to the dashboard where you can manage attendance.

### 7. Testing the Application

Once the application is running, you can:

- Add students to the system.
- Mark attendance for students in a specific division.
- View monthly attendance reports for each student.

### 8. Stop the Application

To stop the application, press `Ctrl+C` in the terminal where the server is running.

## Folder Structure

```
attendance-system/
│
├── app.py                # Main application file
├── requirements.txt      # List of Python dependencies
├── templates/            # HTML templates for rendering pages
│   ├── add_student.html  # page to add students in the database
│   ├── dashboard.html    # Dashboard page
│   ├── login.html        # Login page
│   ├── students.html     # Page to view students
│   ├── attendance.html   # Page to mark attendance
│   ├── base.html         # Base template for common layout
|   └── report.html       # Page to view attendance reports
├── static/               # Static files (CSS, JS, images)
├── attendance.db         # SQLite database file (auto-generated)
└── README.md             # Project documentation
```

## Contributing

Feel free to fork this repository, make changes, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
