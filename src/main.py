from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from university import settings
from university.routers import building, audience, student, teacher, course, exam_mark

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(building.router, prefix=settings.API_VERSION)
app.include_router(audience.router, prefix=settings.API_VERSION)
app.include_router(student.router, prefix=settings.API_VERSION)
app.include_router(teacher.router, prefix=settings.API_VERSION)
app.include_router(course.router, prefix=settings.API_VERSION)
app.include_router(exam_mark.router, prefix=settings.API_VERSION)


@app.get("/api/v1/university")
def root():
    return {"message": "Welcome to University"}


