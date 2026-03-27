# MediTrack

MediTrack is a medicine reminder and stock management web application designed to help users track their medication schedules, monitor inventory, and receive timely notifications.

The application integrates scheduling, real-time stock tracking, and email alerts to improve medication adherence and ensure users never miss a dose. Research shows that many patients do not consistently follow prescribed medication schedules, highlighting the importance of such systems. :contentReference[oaicite:0]{index=0}

---

## Live Demo

Access the deployed application:

https://meditrack-bdid.onrender.com

---

## Features

### Authentication
- Secure user registration and login
- Password hashing using bcrypt
- User-specific data isolation

### Medicine Management
- Add medicines with dosage and schedule
- Track available stock
- Refill and delete medicines
- Real-time stock updates

### Reminder System
- Scheduled email reminders
- Background job processing using APScheduler
- Daily reminder support

### Stock Management
- Automatic calculation of:
  - Doses per day
  - Days of stock remaining
- Status indicators:
  - In Stock
  - Low Stock
  - Out of Stock
- Refill alerts based on thresholds

### Dashboard and Insights
- Central dashboard displaying all medicines
- Stock summary page with categorized views:
  - Critical (0 stock)
  - Low stock
  - Refill soon
  - Well stocked

### Advanced Tracking
- Countdown timer for next dose
- Missed dose detection
- Dynamic UI updates using AJAX

### Notifications
- Reminder emails
- Low stock alerts
- Dose taken confirmation emails

---

## Tech Stack

### Backend
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- APScheduler

### Frontend
- HTML
- CSS
- JavaScript

### Database
- SQLite

### Email Service
- Gmail SMTP / Brevo SMTP

---

## Project Structure

app/
│── models/
│ ├── init.py
│ ├── medicine.py
│ ├── reminder.py
│ └── user.py
│
│── notifications/
│ ├── init.py
│ └── email_sender.py
│
│── routes/
│ ├── auth.py
│ ├── dashboard.py
│ ├── medicines.py
│ └── stock.py
│
│── scheduler/
│ ├── init.py
│ └── jobs.py
│
│── static/
│ ├── main.js
│ └── style.css
│
│── templates/
│ ├── add_medicine.html
│ ├── base.html
│ ├── dashboard.html
│ ├── edit_profile.html
│ ├── login.html
│ ├── register.html
│ └── stock_summary.html
│
├── config.py
├── requirements.txt
├── run.py
└── .gitignore


---

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/diutimaya/MediTrack.git
cd MediTrack

### 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure environment variables

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com

### 5. Run the application

python run.py

## Application Workflow

- Users register and log in securely  
- Medicines are added with schedules and stock details  
- Background scheduler checks reminders periodically  
- Emails are sent at scheduled times  
- Stock is updated when doses are taken  
- Alerts are triggered when stock is low  

---

## Key Functionalities

- Taking a dose reduces stock and logs the action  
- Refilling increases available stock  
- Missed doses are detected after a defined time window  
- Countdown timers display upcoming reminders  

---

## Future Enhancements

- Edit medicine details  
- Multiple reminders per day  
- Dose history analytics  
- Push notifications  
- Mobile application support  

---

## Project Type

Full Stack Healthcare Web Application  

---

## Author

Diutimaya Mohanty  