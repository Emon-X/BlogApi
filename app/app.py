from fastapi import FastAPI
from app.routes import blog,auth,admin
from app.database.db import Base,engine
from fastapi.openapi.utils import get_openapi
from app.services.admin import create_admin

app = FastAPI(
    title="Blog API",
    description="This is a simple Blog API built with FastAPI.",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    create_admin()

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(admin.router)

def custom_openapi():
    
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Blog API",
        version="1.0.0",
        description="This is a simple Blog API built with FastAPI.",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer":{
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token in the format: Bearer <token>"
        }
    }
    
    for path, methods in openapi_schema.get("paths", {}).items():
        if "/auth" not in path and path!="/":
            for method in methods.values():
                if isinstance(method,dict):
                    method["security"] = [{"Bearer": []}]
   
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def Home_Page():
    return {"message": "Welcome to the my Blog!"}