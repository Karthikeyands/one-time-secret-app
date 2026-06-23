# 🔐 One-Time Secret App

A secure API for sharing secrets that can only be viewed **once**, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL (Neon Cloud)**. Secrets are encrypted at rest and permanently deleted after being retrieved.

---

## 🚀 Features

- 🔒 AES encryption via Fernet — secrets are unreadable in the database
- 🧨 Self-destruct after one retrieval — gone forever
- 🔐 Optional password protection (bcrypt hashed)
- 🕒 Optional expiration after set minutes
- ☁️ Neon serverless PostgreSQL — no local DB setup needed
- 📄 Auto-generated Swagger UI at `/docs`

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone <repo-url>
cd one-time-secret-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
ENCRYPTION_KEY=your-generated-key-here
POS_SQL=your-neon-postgresql-url-here
```

#### Generate the ENCRYPTION_KEY

Run this command to generate a valid key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the output and paste it as the value of `ENCRYPTION_KEY` in your `.env` file.

#### Get the POS_SQL URL

- Go to [neon.tech](https://neon.tech)
- Create a project and database
- Copy the connection string (looks like `postgresql://user:password@host/dbname?sslmode=require`)
- Paste it as the value of `POS_SQL`

### 4. Create the Database Table

Run this SQL in your **Neon dashboard → SQL Editor**:

```sql
CREATE TABLE secrets (
    id VARCHAR PRIMARY KEY,
    encrypted_secret VARCHAR NOT NULL,
    password_hash VARCHAR,
    expire_after_minutes INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    viewed BOOLEAN DEFAULT FALSE
);
```

Or use Alembic migrations:

```bash
alembic upgrade head
```

### 5. Run the App

```bash
uvicorn app.main:app --reload
```

You should see:

```
✅ PostgreSQL is available.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 6. Open Swagger UI

Go to 👉 `http://localhost:8000/docs`

Test your endpoints directly from the browser.

---

## 📬 API Usage

### 📤 Create a Secret

```http
POST /secret
```

**Request Body:**

```json
{
  "secret": "my super secret message",
  "password": "optional-password",
  "expire_after_minutes": 10
}
```

**Response:**

```json
{
  "url": "http://localhost:8000/secret/a3f9b2c1-4d5e-6f7a-8b9c-0d1e2f3a4b5c"
}
```

---

### 📥 Access a Secret

```http
POST /secret/access
```

**Request Body:**

```json
{
  "secret_id": "a3f9b2c1-4d5e-6f7a-8b9c-0d1e2f3a4b5c",
  "password": "optional-password"
}
```

**Response:**

```json
{
  "secret": "my super secret message"
}
```

> ⚠️ The secret is **permanently deleted** after this request. Accessing it again returns 404.

---

## 📁 Project Structure

```
one-time-secret-app/
├── alembic/            # DB migration scripts
├── app/
│   ├── crypto.py       # Fernet encrypt/decrypt
│   ├── db.py           # DB connection and session
│   ├── main.py         # FastAPI entry point
│   ├── models.py       # SQLAlchemy table definition
│   └── routes.py       # API endpoints
├── tests/              # Pytest test suite
├── .env                # Environment variables (never commit this)
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## 🧪 Running Tests

```bash
pytest
```

Tests run with `TESTING=1` so no DB connection is required.

---

## 📜 License

MIT License
