Fullstack Todo example (Django + Graphene + NextJS/React + Apollo)
---------------------------------------------------------

Backend (Django):
- cd backend
- uv sync
- source .venv/bin/activate   # or .venv\Scripts\activate on Windows
- python manage.py migrate
- python manage.py runserver 8000
- GraphiQL: http://localhost:8000/graphql/

Frontend (React):
- cd frontend
- npm install
- npm start (http://localhost:3000)

Backend (Django + Graphene) details:
- Requirements:
    - Python 3.11+
    - Django, graphene-django, django-cors-headers
- Environment:
    - Create .env (DJANGO_SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASE_URL)
    - Configure settings.py:
        - INSTALLED_APPS: django.contrib.*, graphene_django, corsheaders, app modules
        - MIDDLEWARE: corsheaders.middleware.CorsMiddleware before CommonMiddleware
        - GRAPHENE settings: SCHEMA = "backend.schema.schema"
        - CORS_ALLOW_ALL_ORIGINS = True (or explicit origins)
- Database:
    - Default uses SQLite; to use Postgres set DATABASE_URL and install psycopg
    - Run migrations before starting the server
- GraphQL schema:
    - schema.py defines Query and Mutation root types
    - Types with graphene.ObjectType map to Django models via DjangoObjectType
    - Resolve methods handle filtering, permissions, and business logic
- Common operations:
    - Queries: list items, retrieve by id, filter by status/text
    - Mutations: create/update/delete items; return payloads and errors
    - Input types: use graphene.InputObjectType for structured mutation args
- Authentication:
    - Enable session or token-based auth
    - Use info.context.user in resolvers; guard mutations with is_authenticated
    - Optionally add login/logout mutations or JWT (via django-graphql-jwt)
- Pagination and filtering:
    - Use relay.Connection for cursor-based pagination
    - Or implement offset/limit manually on Query fields
    - Expose filter args (search, completed, ordering)
- Error handling:
    - Validate inputs; raise GraphQLError for user-facing messages
    - Return structured errors in mutation payloads
- Performance:
    - Use select_related/prefetch_related in resolvers
    - Batch database access; avoid N+1 queries
- Testing:
    - Use graphene test client to assert query/mutation responses
    - Write unit tests for resolvers and permissions
- Deployment:
    - Run with gunicorn/uvicorn (ASGI via channels optional)
    - Apply database migrations on deploy
    - Configure CORS for frontend origin and HTTPS
- Tips:
    - Keep resolvers thin; move logic to services
    - Version schema changes and document breaking changes
    - Enable GraphiQL in development only