Publised on the University server (given Server)
Best way to interact with the web server 
http://group4.com3033.csee-systems.com/ ( With University vpn only or remote access)

########################################################
**Optioon 2 (Run with django virtual environment)**


1️⃣ Clone the repository

git clone https://github.com/Safayet-xx/Exchange_.git
cd Exchange_

2️⃣ Create a virtual environment
Windows
python -m venv venv

macOS / Linux
python3 -m venv venv

3️⃣ Activate the virtual environment
Windows (CMD / PowerShell)
venv\Scripts\activate


You should now see (venv) in the terminal.

macOS / Linux
source venv/bin/activate

4️⃣ Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

5️⃣ Create environment file

Copy the example environment file:

Windows
copy .env.example .env

macOS / Linux
cp .env.example .env


ℹ️ By default, this uses SQLite and console email backend, so no external services are required.

6️⃣ Apply database migrations
python manage.py migrate

7️⃣ Create a superuser (admin)
python manage.py createsuperuser


Follow the prompts to set email and password.

8️⃣ Run the development server
python manage.py runserver

9️⃣ Open the application
Emails are printed to the terminal using:
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend


EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend


OTP codes will appear in the console output when signing up or resetting passwords


##############################################################
**Option 3 with container (Docker COntainer)**

1) Clone
git clone https://github.com/Safayet-xx/Exchange_.git
cd Exchange_

2) Create .env

   
copy .env.docker.example .env

4) Run Docker

docker compose up -d --build

5) Migrate

docker compose exec web python manage.py migrate

