# School Website Project

A modern, Flask-based school website project designed for educational institutions. It includes public-facing pages for admissions, academics, gallery, notices, events, and a contact system, along with an admin dashboard for managing the website content. The project also includes an automated email notification system and support for cloud-based image/media usage for school imagery.

## Overview

This project serves as a full-featured starter for developing a school or academy website. It is built using Flask and SQLAlchemy and is organized to support both public website visitors and school administrators.

It includes:

- A clean landing page for the school
- About, academics, and admission pages
- Event and notice management
- Contact form with automated email response
- Admission inquiry form with email alerts
- Admin login and dashboard
- Image gallery and media management support
- Cloudinary-ready media handling for school photos and banners

## Features

### Public website pages

- Home page with hero section and school highlights
- About page with vision, history, principal message, and values
- Academics page with curriculum and educational overview
- Admission page with process details and application form
- Contact page with office information and enquiry form
- Gallery page for school images and videos
- Events and notices section

### Admin dashboard

- Secure login for administrators
- Manage major site sections and content
- Update notices, events, galleries, and academic information
- View and manage contact and admission queries
- Configure school details from a centralized dashboard

### Automated email system

- Contact form submissions trigger email notifications
- Admission submissions trigger email notifications
- SMTP-based sending using Gmail App Passwords
- HTML-formatted email templates for school administration

### Media and image support

- Local static assets are included for development
- The project is structured to support cloud-based image hosting
- Images can be used for school banners, gallery content, principal photos, and academic visuals
- Cloudinary integration is suitable for efficient upload, optimization, and delivery of images

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- HTML
- CSS
- JavaScript
- SQLite (default setup)
- SMTP email sending (Gmail-compatible)
- Cloudinary-ready media pipeline

## Project Structure

```text
school-website-project/
├── app.py
├── models.py
├── email_function.py
├── requirements.txt
├── __init__.py
├── instance/
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── templates/
│   ├── about.html
│   ├── academics.html
│   ├── admission.html
│   ├── contact.html
│   ├── dashboard.html
│   ├── events-notices.html
│   ├── gallery.html
│   ├── index.html
│   ├── login.html
│   ├── navbar.html
│   ├── footer.html
│   └── ...
└── README.md
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.9+
- pip
- Virtual environment support
- A Gmail account (if using SMTP email sending)
- Optional: Cloudinary account for media hosting

## Installation

1. Clone the repository

```bash
git clone https://github.com/code-with-emptyness/school-website-project.git
cd school-website-project
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Initialize the database

The project uses Flask-SQLAlchemy models. Run the app once so the database can be created, or initialize the database through your preferred Flask setup.

## Configuration

### Email setup

Create a file named `credentials.env` in the project root with the following values:

```env
SMTP_EMAIL=your-email@gmail.com
SMTP_RECEIVER=admin@your-school.com
SMTP_APP_PASSWORD=your-google-app-password
```

Notes:

- Use a Gmail App Password for the SMTP connection.
- Enable 2-Step Verification on the Gmail account before generating the app password.
- Keep this file private and do not commit it to version control.

### Cloudinary / image setup

If you plan to upload or host school images using Cloudinary, add your Cloudinary configuration in your environment or app settings:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

This allows the project to support cloud-based picture storage for hero banners, student photographs, gallery images, and other media assets.

## Run the application

```bash
python app.py
```

Then open the project in your browser:

```text
http://127.0.0.1:5000
```

## Important Notes

- The project is best suited for educational institutions, schools, and academies.
- Email sending will only work correctly when valid SMTP credentials are configured.
- For production deployment, use secure environment variables and never hardcode secrets into source code.
- If using Cloudinary, optimize image sizes and configure caching for faster delivery.

## Suggested future enhancements

- Add role-based access control for admin users
- Add real Cloudinary uploads via Flask forms
- Add export support for inquiry records
- Add PDF generation for admission forms
- Add better deployment support for Docker or Render/Vercel
- Add unit tests and CI pipeline

## License

This project is provided for educational and development purposes. Please check the repository license if one is added later.

## Contributing

Contributions are welcome. If you want to improve the project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

## Contact

For project-related questions or school website customization, please contact the repository owner or project maintainer.

---

This README is designed to help developers understand the project structure, setup requirements, and the key features such as automatic email notifications and cloud-based image usage for a school website.
