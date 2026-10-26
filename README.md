# St. Xavier's School Website

A modern, responsive school management and website project built with Flask. It includes public-facing pages for a school website as well as an admin dashboard for updating content, managing notices, events, galleries, academic information, and handling student enquiries.

This project is designed to help schools present themselves online with a professional layout, easy content management, and built-in communication features.

## Highlights

- Beautiful school landing page with hero content and highlights
- About page with values, vision, history, and principal message
- Academics section with curriculum and topper showcases
- Admissions page with application flow and form
- Contact page with school information and enquiry form
- Notice and event management sections
- Gallery for school activities and media
- Admin dashboard for content updates
- Automated email notifications for contact and admission queries
- Media-friendly design for cloud-hosted imagery and banners

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML, CSS, JavaScript
- SMTP email sending via Gmail App Passwords
- Cloudinary-compatible media workflows

## Project Structure

```text
school-website-project/
├── app.py
├── models.py
├── email_function.py
├── requirements.txt
├── __init__.py
├── README.md
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
│   ├── footer.html
│   ├── gallery.html
│   ├── index.html
│   ├── login.html
│   ├── navbar.html
│   └── under_development.html
└── database.db   # generated locally when running the app
```

## Features

### Website pages

- Home page with school branding and key messages
- About Us section with founder/principal message and institutional values
- Academics page for curriculum and school strengths
- Admission page for enrollment process and application form
- Contact page with map, office timings, and FAQs
- Events and notices section for upcoming activities
- Gallery page supporting photo and video content

### Admin dashboard

- Secure admin login
- Edit hero content, facilities, values, and vision
- Manage page sections with dynamic forms
- Add or edit notices, events, calendars, and gallery items
- Review contact and admission enquiries
- Update school configuration and page content from one place

### Automated email notifications

The project sends HTML emails whenever a user submits:

- a contact form enquiry
- an admission inquiry

This is handled through the SMTP configuration in `email_function.py`.

### Image handling and Cloud usage

The site supports uploading and displaying school images locally and is structured to work with cloud-hosted media services such as Cloudinary for production use.

This is useful for:

- gallery images
- hero banners
- principal and staff images
- event and campus imagery

## Getting Started

### 1) Clone the repository

```bash
git clone https://github.com/code-with-emptyness/school-website-project.git
cd school-website-project
```

### 2) Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- macOS/Linux:

```bash
source venv/bin/activate
```

- Windows:

```bash
venv\Scripts\activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a file named `credentials.env` in the project root and add the SMTP credentials:

```env
SMTP_EMAIL=your-email@gmail.com
SMTP_RECEIVER=school-admin@example.com
SMTP_APP_PASSWORD=your-google-app-password
```

Notes:

- Use a Gmail App Password, not your regular account password.
- Ensure 2-Step Verification is enabled on the Gmail account.
- Keep this file private and never commit it to source control.

Optional Cloudinary configuration for image hosting:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Running the Project

```bash
python app.py
```

Then open the site in your browser:

```text
http://127.0.0.1:8000
```

## Default Admin Credentials

For local testing, the app seeds a default admin account:

- Username: `admin`
- Password: `admin123`

Important: change this in production before deployment.

## Deployment Notes

For production deployment:

- use environment variables instead of hardcoded secrets
- set up a secure database backend if needed
- configure a real SMTP service
- enable Cloudinary or another media solution for production image hosting
- restrict admin access behind authentication and proper server security

## Contributing

Contributions are welcome. If you'd like to improve the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit and push your branch
5. Open a pull request

## License

This project is provided for educational and development purposes. Please check the repository for license details before using it in a production or commercial setting.

## Contact

For collaboration, updates, or school website customization requests, reach out through the repository owner or maintainer.

---

This project is a strong starting point for building a professional school website with modern front-end presentation, administrative content management, and automated communication workflows.
