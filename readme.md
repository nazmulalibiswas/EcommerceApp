# Capstone Ecommerce Projects
- This is a ecommerce web application projects which is run by decoupled architectuere
Frontend: React, HTML, CSS, Tailwind
Backend: Django, DRF, JWT Auth
Database: Postgresql

# 1. Quick Installation Guidelines
## Git Clone
- `git clone "repo link"`

## CD Frontend
- go to the directory of frontend and 
  - `npm install`
  - `npm run dev`

## CD Backend
- go to the directory of backend and 
  - `cd backend`
  - `python -m venv env`
  -  `env\Scripts\activate`

### 2. Install Dependencies
Make sure all necessary packages are installed. If there is a `requirements.txt` file in the folder, run:
```bash
pip install -r requirements.txt
```
### 3. Apply Database Migrations
To ensure your local `db.sqlite3` database has all the necessary tables for the blog, run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create or Run a Superuser (Admin Account)
To manage blog posts, categories, and users, you need an admin account.(username, email, password):
- Admin Account (Superuser)
A superuser account is already created and saved in the included db.sqlite3 database. You can use the following credentials to access the admin dashboard:
- Username: admin 
- Password: admin
- (If you ever need to create another admin account, you can run: python manage.py createsuperuser)

### 5. Run the Local Server
Now you are ready to start the application! Run the following command:
```bash
npm run dev
python manage.py runserver
```
### 6. View the Project in Your Browser
Open your favorite web browser and go to:
- **Frontend:** [http://localhost:5173/](http://localhost:5173/)
- **Main Website:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Dashboard:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin) (Log in with the superuser account you just created).

# Contributor
1. Md. Nazmul Ali Biswas (nazmulalibiswas)
- Fullstack Engineer & Tech Enthusiast
- Contact: nazmulalibiswas.dev@gmail.com
2. Md. Torikul Islam
- Data Engineer & Tech Enthusiast
- Contact: dataengineertorikulislam@gmail.com

