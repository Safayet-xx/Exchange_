╔════════════════════════════════════════════════════════╗
║         Exchange Platform - Quick Start                ║
╚════════════════════════════════════════════════════════╝

STEP 1: Run Setup
─────────────────
Double-click:
    SETUP.bat

This creates the database and test users.


STEP 2: Start Server
─────────────────────
Run:
    python manage.py runserver

Or:
    py manage.py runserver


STEP 3: Visit Site
──────────────────
Open browser:
    http://127.0.0.1:8000/


STEP 4: Login
─────────────
Use any test account:
    Email: student1@brunel.ac.uk
    Email: student2@brunel.ac.uk
    Email: prof1@brunel.ac.uk
    Password: testpass123


═══════════════════════════════════════════════════════

TROUBLESHOOTING
───────────────

"No such table" error?
→ You forgot to run SETUP.bat first!

"Port already in use"?
→ Run: python manage.py runserver 8080

"Module not found"?
→ Run: pip install -r requirements.txt

Still not working?
→ Delete db.sqlite3 and run SETUP.bat again

═══════════════════════════════════════════════════════

For detailed documentation, see:
    README_FIXED.md

═══════════════════════════════════════════════════════
