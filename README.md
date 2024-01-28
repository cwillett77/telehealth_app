# Telehealth App

## Description

This Django-based telehealth application provides a platform for online medical consultations. It includes features like appointment scheduling, real-time video conferencing, and secure messaging, making healthcare more accessible and efficient.

## Key Features

- Patient and Doctor registration and management
- Appointment booking system
- Real-time video conferencing
- Secure chat functionality
- Responsive web design

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   `gh repo clone cwillett77/telehealth_app`
   or
   `https://github.com/cwillett77/telehealth_app.git`

2. Navigate to the project directory:
   `cd telehealth_app`

3. Create a virtual environment:
   `python -m venv venv`

4. Activate the virtual environment:

- On Windows: `venv\Scripts\activate`
- On Unix or MacOS: `source venv/bin/activate`

5. Install dependencies:
   `pip install -r requirements.txt`

6. Run database migrations:

```
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser (for admin access):
   `python manage.py createsuperuser`

8. Run the development server:
   `python manage.py runserver`

## Usage

After starting the server, access the app at `http://localhost:8000`. Use the admin panel at `http://localhost:8000/admin` to manage the application.

For further details on each feature and API endpoints, refer to the documentation within each app module.

## Contributing

Contributions to the project are welcome. Please fork the repository and submit a pull request with your proposed changes.

## License

[MIT License](LICENSE.md)
