# Django To-Do List Application

## Overview

This is a simple yet effective To-Do List application built using Django. Users can register, log in, manage their tasks, and update their profiles, including uploading a profile picture. The application features a clean user interface and provides functionality for task management, including adding, updating, and deleting tasks.

## Features

- User registration and login/logout functionality.
- Create, update, and delete tasks.
- Each task includes a title and a message.
- Tasks are associated with users.
- Profile picture upload during user registration.
- Responsive design for a better user experience.
- Flash messages for user feedback on actions.

## Technologies Used

- Django
- Python
- HTML/CSS
- JavaScript
- SQLite (default database)

## Installation

### Prerequisites

Make sure you have Python and pip installed on your system.

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/todo-list-app.git
   cd todo-list-app

2. **Create a Virtual Environment:**


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Requirements:**


pip install -r requirements.txt

4. **Run Migrations:**


python manage.py migrate

5. **Create a Superuser (Optional):**


python manage.py createsuperuser

6. **Run the Development Server:**


python manage.py runserver

7. **Access the Application: Open your web browser and go to http://127.0.0.1:8000/.

**Usage**

Registration: Users can create a new account by providing a username, password, and profile picture.
Login: Registered users can log in using their credentials.
Task Management: Users can add new tasks, update existing tasks, and delete tasks as needed.
Profile Update: Users can update their profile information, including their profile picture.

## Contributing

**Fork the repository.**
Create a new branch (git checkout -b feature/YourFeature).
Make your changes and commit them (git commit -m 'Add some feature').
Push to the branch (git push origin feature/YourFeature).
Create a new Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Contact
For any inquiries or feedback, please contact:

Name: Stephen Ongera
Email: gadafisteve001@gmail.com

**Acknowledgements**
Thanks to the Django community for their excellent framework and documentation.



### Customization

- **Repository URL**: Replace `https://github.com/yourusername/todo-list-app.git` with the actual URL of your project repository.
- **Email**: Change `gadafisteve001@gmail.com` to your actual email address.
- **License**: If you use a different license, update the license section accordingly.

### How to Save

Create a file named `README.md` in your project root and copy-paste the content above. This will provide clear instructions and details about your project for anyone who wants to use or contribute to it.





