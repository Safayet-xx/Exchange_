
) Clone repo
git clone https://github.com/Safayet-xx/Exchange_.git
cd Exchange_

2) Create .env from example (Windows CMD)
copy .env.docker.example .env

3) Build + run
docker compose up -d --build

4) Run migrations
docker compose exec web python manage.py migrate

The application is deployed and accessible at:

http://group4.com3033.csee-systems.com/ ( With University vpn only or remote access)
