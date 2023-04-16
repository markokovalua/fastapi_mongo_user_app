`Darqube task description:`

Framework: FastApi
Database: MongoDB(driver: motor)
Deploy: Docker Compose

1. Create a user model using Pydantic with following attributes:
        id
        first_name
        last_name
        role (one of: admin, dev, simple mortal)
        is_active
        created_at
        last_login
        hashed_pass

2. Define and implement validation strategy for each one of given fields.
3. Implement REST API methods for users using the already defined Pydantic model.
4. Implement a simple authentication middleware.
5. Create a route restricted only for user's with admin roles which allow to change by oid(ObjectId) other user's attributes except `hashed_pass`.
6. Create a docker-compose file to deploy the app.
7. Upload the solution to github and send the link.

`to run project run in docker-compose directory the following command:`

docker-compose up -d

`use endpoint /redoc in browser to see possible API endpoints and their params`