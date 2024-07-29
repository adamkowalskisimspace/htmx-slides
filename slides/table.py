import random
import asyncio
from typing import TypedDict
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


class Person(TypedDict):
    first: str
    last: str
    age: int


people: list[Person] = [
    {"first": "Bob", "last": "Smith", "age": 32},
    {"first": "Joe", "last": "Johnson", "age": 28},
    {"first": "Sally", "last": "Carter", "age": 35},
    {"first": "Jane", "last": "Doe", "age": 45},
    {"first": "Mike", "last": "Meyers", "age": 55},
    {"first": "John", "last": "Doe", "age": 21},
]


def filtered_people(search: str) -> list[Person]:
    filtered: list[Person] = []
    for person in people:
        first = person["first"].lower()
        if first.startswith(search):
            filtered.append(person)
    return filtered


@router.get("/table", response_class=HTMLResponse)
async def read_table(request: Request):
    data = request.query_params
    search = data.get("search")
    if search is None:
        print("sleeping")
        sleep_time = random.randint(1, 2)
        await asyncio.sleep(sleep_time)
        search = ""
    people = filtered_people(search.lower())
    return templates.TemplateResponse(
        request=request,
        name=f"/table.html",
        context={"people": people},
    )
