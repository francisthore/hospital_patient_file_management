# Hospital Patient File Management System

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

![Screenshot of project dashboard](https://francisthore.github.io/static/img/project%20hero.png)

## Description
The Hospital Patient File Management System is designed to help medical institutions efficiently manage patient files. It aims to reduce patient waiting times by enabling quick retrieval of patient records with just a few clicks, rather than through physical searches. This project is especially beneficial for South Africa's struggling medical institutions.

The system features role-based access control to ensure data security. For instance, a receptionist can only check if a patient exists and register them if they don't.

You can see the project demo here [https://app.thore.tech](https://app.thore.tech) and read a more in depth blog post on [LinkedIn](https://www.linkedin.com/pulse/clinic-queues-most-african-countries-finally-coming-end-francis-thore-lp6df/?trackingId=I4f5unmwQXue6HnPpzGK1A%3D%3D)

The project is built using the **Python Flask Framework**.

## Installation

1. **Clone the repo**
    ```bash
    git clone https://github.com/francisthore/hospital_patient_file_management.git
    ```

2. **Create a Python virtual environment**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**
    ```bash
    source venv/bin/activate
    ```

4. **Navigate to the project directory**
    ```bash
    cd hospital_patient_file_management
    ```

5. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

6. **Set up environment variables**
    ```bash
    vi .env
    ```

    **Define these variables in the `.env` file:**
    ```plaintext
    DB_USERNAME=username
    DB_PASSWORD=pwd
    DB_NAME=name
    DB_HOST=host
    MAIN_APP_KEY=key_here
    MAIN_API_KEY=key_here
    ```

    **Note:** You need to define API keys and Mailgun domain.

7. **Run the API and app**
    ```bash
    python -m api.v1.app
    python -m main_app.app
    ```

    **Note:** Use WSGI or Gunicorn for production.

## Usage

Access the app via your browser on the port that the main app is running on. For production, set up Nginx as a reverse proxy for the Flask app.

## Features

1. **Registration**
    - Users can register via the web form on the register route.
    - Email verification is required.

2. **Login**
    - After registration, users can log in.
    - Initially, users can only view their profile.

3. **Role-Based Access Control**
    - Admins can manually update user roles in the database.
    - Assigned roles determine the user's access to patient data.

4. **Pending Features**
    - Institution-based registration
    - Cross-institution data access
    - Password reset
    - Two-factor authentication
    - Advanced search queries

## Contributing

I welcome contributors to help improve this project.

1. Fork the project
2. Create your feature branch
    ```bash
    git checkout -b your_feature
    ```
3. Commit your changes
    ```bash
    git commit -m 'Add AmazingFeature'
    ```
4. Push to the branch
    ```bash
    git push origin your_feature
    ```
5. Open a Pull Request


## Related projects
1. [Hospital Management System by Kisharn](https://github.com/kishan0725/Hospital-Management-System)
2. [Hospital Management System by Opensource-emr](https://github.com/opensource-emr/hospital-management-emr)

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Francis Thore - [thorefrancis@gmail.com](mailto:thorefrancis@gmail.com)  
Project Link: [github.com/francisthore/hospital_patient_file_management](https://github.com/francisthore/hospital_patient_file_management)
