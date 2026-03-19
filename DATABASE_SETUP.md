# Database Setup Guide

## MySQL Workbench Setup

### Step 1: Open MySQL Workbench
- Launch MySQL Workbench on your computer

### Step 2: Create a Connection
- Click on the "+" icon to create a new connection
- Fill in the details:
  - Connection Name: `BookMyShoot`
  - Hostname: `localhost`
  - Port: `3306`
  - Username: `root` (or your MySQL username)
  - Password: Click "Store in Vault" to enter your password

### Step 3: Connect to MySQL Server
- Double-click the connection to connect

### Step 4: Create Database
Run the following SQL command in the query editor:

```sql
CREATE DATABASE bookmyshoot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bookmyshoot;
```

### Step 5: Update Backend Configuration

Edit `backend/config.py` and uncomment the MySQL configuration:

```python
# MySQL Configuration
DATABASE_URI = 'mysql://root:your_password@localhost/bookmyshoot'
```

Replace `your_password` with your actual MySQL password.

### Step 6: Install MySQL Python Package

```bash
pip install pymysql
```

### Step 7: Run the Backend

```bash
cd backend
python app.py
```

The database tables will be created automatically.

---

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `GET /api/user/<id>` - Get user details

### Bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings/<id>` - Get booking details
- `GET /api/bookings/customer/<id>` - Get customer's bookings
- `GET /api/bookings/photographer/<id>` - Get photographer's bookings
- `PUT /api/bookings/<id>/status` - Update booking status

### Payments
- `POST /api/payments` - Process payment
- `GET /api/payments/booking/<id>` - Get booking payments

### Photographers
- `GET /api/photographers` - List all photographers
- `GET /api/photographers/<id>` - Get photographer details
- `GET /api/photographers/revenue/<id>` - Get photographer revenue

### Statistics
- `GET /api/stats/customer/<id>` - Get customer statistics

---

## Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| first_name | VARCHAR(100) | User's first name |
| last_name | VARCHAR(100) | User's last name |
| email | VARCHAR(120) | Unique email |
| phone | VARCHAR(20) | Phone number |
| user_type | VARCHAR(20) | 'customer' or 'photographer' |
| password_hash | VARCHAR(255) | Hashed password |
| is_active | BOOLEAN | Account status |
| created_at | DATETIME | Creation timestamp |

### Photographers Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| user_id | INT | Foreign key to users |
| specialty | VARCHAR(100) | Photography specialty |
| hourly_rate | FLOAT | Rate per hour |
| bio | TEXT | Bio description |
| is_available | BOOLEAN | Availability status |

### Bookings Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| customer_id | INT | Foreign key to users |
| photographer_id | INT | Foreign key to photographers |
| service_type | VARCHAR(50) | Type of service |
| event_date | DATE | Event date |
| event_time | VARCHAR(20) | Event time |
| location | VARCHAR(255) | Event location |
| notes | TEXT | Additional notes |
| total_price | FLOAT | Total price |
| token_amount | FLOAT | 30% token amount |
| remaining_amount | FLOAT | Remaining 70% |
| status | VARCHAR(20) | pending/accepted/declined/completed |
| payment_status | VARCHAR(20) | pending/token_paid/paid |

### Payments Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| booking_id | INT | Foreign key to bookings |
| customer_id | INT | Foreign key to users |
| photographer_id | INT | Foreign key to photographers |
| amount | FLOAT | Payment amount |
| payment_type | VARCHAR(20) | token/remaining/full |
| payment_method | VARCHAR(50) | Payment method |
| transaction_id | VARCHAR(100) | Unique transaction ID |
| status | VARCHAR(20) | pending/completed/failed |
| created_at | DATETIME | Payment timestamp |
