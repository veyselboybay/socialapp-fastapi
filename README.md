# Project Description
- Developed a back end api using `FastAPI and Postgresql`. 
- Alembic is used for database migrations
- Users can register and login using the api via Postman or built-in Swagger. 
- Users are also able to perform CRUD operations for creating, reading, updating or deleting a post within their account.
# Installation
- Download or git clone `<project-url>`
- After having the code in your machine, 
    1. Run `pip install -r requirements.txt` in root directory -> this will install all necessary dependencies
    2. Create an `.env` file inside the root directory with the following content:
        -  `DB_CONNECTION`= `<your-db-connection-url>` -> (e.g. -> postgresql://`<username>`:`<password>`@localhost:5432/`<db-name>`)
        - `SECRET` = `<your-secret>` -> This one is for jwt
        - `ALGORITHM` = HS256
        - `EXPIRES_IN` = 30
# How to Run
- Run `uvicorn app.main:app --reload` command in root directory
- Open your internet browser and go to `http://localhost:8000/docs`-> this will open the built-in Swagger UI to perform operations

# Future Reference
- If you want to modify db models or add new ones, you have to run the migrations in order to use your new db models. To do that, in your root directory run the codes below for successful db migrations.
    1. `alembic revision --autogenerate -m 'Write your message here'`
    2. `alembic upgrade head`
