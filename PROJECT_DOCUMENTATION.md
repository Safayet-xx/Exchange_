# 🎓 Exchange Platform - Complete Implementation Documentation

## 📌 Project Overview

A university skill exchange platform where students and professors help each other using credits instead of money. Everyone starts with 10 credits and earns more by helping others.

---

## 🏗️ Complete Architecture

### Database Models

#### 1. User (accounts.User)
```python
- email (unique, CharField)
- email_verified (Boolean)
- password (hashed)
- date_joined (DateTime)
- is_active (Boolean)
- is_staff (Boolean)
- is_superuser (Boolean)
```

#### 2. OTP (accounts.OTP)
```python
- user (ForeignKey to User)
- code (6 digits)
- purpose (signup/login/reset)
- created_at (DateTime)
- expires_at (DateTime)
- is_used (Boolean)
- last_sent (DateTime)
```

#### 3. Profile (profiles.Profile)
```python
- user (OneToOne User)
- role (student/professor)
- full_name
- handle (unique slug)
- display_name
- email_verified
- is_completed
+ avatar (ImageField) - TODO
```

#### 4. Endorsement (profiles.Endorsement)
```python
- professor (ForeignKey User)
- student (ForeignKey User)
- rating (1-5)
- comment
- created_at
```

#### 5. CreditWallet (credits.CreditWallet)
```python
- user (OneToOne User)
- balance (default 10)
```

#### 6. CreditTransaction (credits.CreditTransaction)
```python
- from_user (ForeignKey User)
- to_user (ForeignKey User)
- amount
- note
- session (ForeignKey Session, optional)
- created_at
```

#### 7. Skill (skills.Skill)
```python
- name (unique)
```

#### 8. UserSkill (skills.UserSkill)
```python
- user (ForeignKey User)
- kind (offer/want)
- skills (ManyToMany Skill)
- title
- description
- is_active
- created_at
```

#### 9. Session (exchanges.Session)
```python
- requester (ForeignKey User)
- helper (ForeignKey User)
- title
- description
- agreed_amount
- status (pending/accepted/completed/cancelled)
- credits_transferred (Boolean)
- created_at
- updated_at
```

---

## 🔄 User Flow Diagrams

### Registration Flow
```
1. User goes to /accounts/signup/
2. Fills email + password (university domain required)
3. System creates User account (email_verified=False)
4. System generates 6-digit OTP
5. OTP sent to email (in dev: shown in console)
6. User enters OTP at /accounts/verify-otp/
7. System verifies OTP
8. User email_verified = True
9. User logged in automatically
10. Redirected to /profiles/setup/
11. User fills profile info (name, handle, role)
12. Profile is_completed = True
13. Redirected to /core/home/
```

### Credit Transfer Flow
```
1. User A goes to /credits/transfer/
2. Searches for User B
3. Enters amount and note
4. System validates:
   - User A has enough balance
   - User A != User B
   - Amount > 0
5. Transaction created in atomic block:
   - User A balance -= amount
   - User B balance += amount
   - CreditTransaction record created
6. Success message shown
7. Redirected to /credits/wallet/
```

### Skill Exchange Flow
```
1. User A posts "Need help with Python" (UserSkill kind=want)
2. User B searches skills, finds User A's post
3. User B contacts User A (via profile)
4. They agree to help session
5. User B creates Session:
   - requester = User A
   - helper = User B
   - agreed_amount = X credits
   - status = pending
6. User A accepts → status = accepted
7. After help is provided
8. User A marks completed:
   - status = completed
   - Credits automatically transferred
   - CreditTransaction created linked to Session
```

---

## 📂 File Structure

```
exchange/
├── exchange/                    # Project settings
│   ├── __init__.py
│   ├── settings.py             # ✅ FIXED
│   ├── urls.py                 # ✅ FIXED
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                    # Authentication
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # User, OTP
│   ├── forms.py                # SignUpForm
│   ├── views.py                # ✅ FIXED
│   ├── urls.py                 # ✅ FIXED
│   ├── middleware.py           # ProfileCompletionMiddleware
│   └── templates/accounts/
│       ├── login.html
│       ├── signup.html
│       └── verify_otp.html
│
├── profiles/                    # User profiles
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Profile, Endorsement
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py              # Auto-create profile
│   └── templates/profiles/
│       ├── profile_setup.html
│       ├── public_profile.html
│       └── user_search.html
│
├── credits/                     # Credit system
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py                 # Auto-create wallet
│   ├── models.py               # CreditWallet, CreditTransaction
│   ├── views.py
│   ├── urls.py
│   ├── signals.py              # ✅ NEW
│   └── templates/credits/
│       ├── wallet.html
│       └── transfer.html
│
├── skills/                      # Skill management
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Skill, UserSkill
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/skills/
│       ├── add.html
│       └── search.html
│
├── exchanges/                   # Help sessions
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Session
│   ├── views.py
│   └── urls.py
│
├── core/                        # Home/Dashboard
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/core/
│       └── home.html
│
├── templates/                   # Global templates
│   └── base.html
│
├── static/                      # Static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                       # User uploads
│   └── avatars/
│
├── manage.py
├── db.sqlite3
├── requirements.txt
├── SETUP_GUIDE.md              # ✅ NEW
└── README.md
```

---

## 🔧 Configuration Files

### requirements.txt
```
Django==5.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
Pillow==10.1.0
```

### .gitignore
```
*.pyc
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
db.sqlite3
db.sqlite3-journal
/media
/staticfiles
/static_collected
.env
.venv
env/
venv/
*.log
.DS_Store
node_modules/
```

---

## ✅ Current Status

### ✅ Completed Features
- [x] User authentication with email
- [x] OTP email verification
- [x] Profile system with roles
- [x] Credit wallet (auto-created)
- [x] Credit transactions
- [x] Skill posts (offer/want)
- [x] User search
- [x] Public profiles
- [x] Session/Exchange system
- [x] Professor endorsements
- [x] Admin panel
- [x] Profile completion middleware
- [x] Transaction history
- [x] University email domain validation

### ⏳ Pending Features
- [ ] REST API endpoints
- [ ] React frontend
- [ ] Real-time notifications
- [ ] Advanced search filters
- [ ] Skill matching algorithm
- [ ] Dispute resolution
- [ ] Email notifications (SMTP)
- [ ] Avatar upload
- [ ] Session chat/messaging
- [ ] Rating aggregation
- [ ] Analytics dashboard

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install django==5.2.7 --break-system-packages
pip install djangorestframework --break-system-packages
pip install django-cors-headers --break-system-packages
pip install Pillow --break-system-packages
```

### 2. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Run Server
```bash
python manage.py runserver
```

### 5. Access Application
- Main site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## 🧪 Testing Scenarios

### Test 1: Complete User Journey
1. Sign up with university email
2. Verify OTP
3. Complete profile
4. Add skills (offers & wants)
5. Search for other users
6. Transfer credits
7. Create exchange session
8. Complete session (credits transfer)
9. Check wallet history

### Test 2: Admin Features
1. Login to admin panel
2. View all users
3. Adjust credit balances
4. Manage endorsements
5. Handle disputes

---

## 🐛 Known Issues & Fixes

### Issue: Middleware redirect loop
**Cause**: ProfileCompletionMiddleware redirecting before profile exists
**Fix**: Ensure profile is created via signals on user creation

### Issue: OTP not sending
**Cause**: EMAIL_BACKEND is console in development
**Solution**: Check console output for OTP codes

### Issue: CORS errors with React
**Cause**: CORS_ALLOWED_ORIGINS not configured
**Fix**: Already added in settings.py

---

## 📊 Database Relationships

```
User (1) ←→ (1) Profile
User (1) ←→ (1) CreditWallet
User (1) ←→ (N) CreditTransaction (as from_user)
User (1) ←→ (N) CreditTransaction (as to_user)
User (1) ←→ (N) UserSkill
User (1) ←→ (N) Session (as requester)
User (1) ←→ (N) Session (as helper)
User (1) ←→ (N) Endorsement (as professor)
User (1) ←→ (N) Endorsement (as student)
User (1) ←→ (N) OTP

Session (1) ←→ (N) CreditTransaction
UserSkill (N) ←→ (N) Skill
```

---

## 🎯 Next Development Phase

### Phase 2: REST API
- Create `api/` app
- Define serializers
- Create ViewSets
- Add token authentication
- Document endpoints

### Phase 3: React Frontend
- Setup Vite + React
- Create components
- Implement routing
- Connect to API
- Add state management (Redux/Zustand)

### Phase 4: Production Deployment
- Switch to PostgreSQL
- Setup Gunicorn
- Configure Nginx
- Setup SSL
- Configure SMTP for emails
- Add monitoring
- Setup backups

---

## 📚 Additional Documentation

See also:
- SETUP_GUIDE.md - Detailed setup instructions
- IMPLEMENTATION_GUIDE.md - Step-by-step development guide
- API_DOCS.md - REST API documentation (coming soon)
