# Multipart Email API with Multiple Recipients & Embedded Image

A Django REST Framework API that sends HTML-formatted emails with embedded images to multiple recipients using multiple email service providers for reliability.

## Features

- **Multipart Email Sending**: Send HTML-formatted emails with embedded images
- **Multiple Email Service Provider Support**:
  - Django's built-in SMTP (Primary)
  - Amazon Simple Email Service (SES) (Fallback)
- **Recipient Validation**: Only allows emails from specific domains (Gmail, Hotmail, Yahoo) and specific addresses (careers@accelx.net)
- **Image Validation**: Validates uploaded images (format, size)
- **Well-Structured HTML Emails**: Professionally formatted HTML emails with styling
- **Error Handling**: Comprehensive error handling and validation
- **Fallback Mechanism**: Attempts multiple providers if one fails

## API Specification

**Endpoint**: `POST /api/send-selection-email/`  
**Request Type**: `multipart/form-data`

**Request Payload**:

| Field         | Type         | Required | Description                               |
|---------------|--------------|----------|-------------------------------------------|
| name          | string       | ✅       | Full name of the candidate                |
| education     | string       | ✅       | Education information                     |
| contact       | string       | ✅       | Phone number                              |
| address       | string       | ✅       | Current address                           |
| project_idea  | string       | ✅       | Description of a personal project idea    |
| screenshot    | file (jpg/png)| ✅      | GitHub profile screenshot (embedded inline)|
| recipients    | list[string] | ✅       | Email addresses (must include allowed domains)|

**Allowed Recipient Domains**:
- @gmail.com
- @hotmail.com
- @yahoo.com
- careers@accelx.net (special allowed address)

**Email Subject Format**:  
`Python Backend Engineer Selection Task - <Your Name>`

**Email Body Format**:
1. Candidate Name, Education, Contact, Address
2. Screenshot image embedded in the center
3. Project idea below the image
4. Neatly formatted with basic styling

## Setup Instructions

### Prerequisites

- Python 3.8+
- Pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/sakibcse11/multipart_email_api.git
   cd multipart_email_api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

5. Configure your email service credentials in the `.env` file:
   ```
   # Primary Email Service (Gmail)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password  # App password for Gmail
   EMAIL_USE_TLS=True
   DEFAULT_FROM_EMAIL=your-email@gmail.com

   # Optional: Backup Email Services
    AWS_ACCESS_KEY_ID=access key from aws
    AWS_SECRET_ACCESS_KEY=access key from aw
    AWS_REGION=region (eg. 'us-east-1')
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```
## Swagger Api docs: http://127.0.0.1:8000/api/docs/swagger/#/api/api_send_selection_email_create


## Response Examples

### Success Response
```json
{
  "status": "success",
  "message": "Email sent to 4 recipients"
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Only Gmail, Hotmail, Yahoo, and careers@accelx.net are allowed. Invalid emails: test@example.com"
}
```

## Architecture

The application follows a clean architecture approach:

1. **API Layer**: Handles HTTP requests/responses (views.py)
2. **Serialization Layer**: Validates request data (serializers.py)
3. **Service Layer**: Contains business logic for sending emails (services.py)
4. **Configuration**: Centralized settings in settings.py

## Security Considerations

- Email service provider credentials are stored in environment variables
- Recipient validation prevents email spam
- File validation prevents upload of malicious content
- Proper error handling to prevent information leakage

## Backup Email Providers

The system attempts to send emails using Django's built-in SMTP first, but if that fails, it will try Amazon SES as fallbacks. This ensures high availability and reliability.
