from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health
from models.book import BookCreate, BookRead, BookUpdate, BookReplace
from models.library import LibraryCreate, LibraryRead, LibraryUpdate, LibraryReplace
from uuid import uuid4

port = int(os.environ.get("FASTAPIPORT", 8000))

persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
books: Dict[UUID, BookRead] = {}
libraries: Dict[UUID, LibraryRead] = {}

def add_data():
    book1 = BookRead(
        # id=uuid4(),
        id=UUID("90143569-66f2-493d-a4a6-b519bb75d10a"),
        title="Tgggg",
        author="Fgggg",
        price=33.33
    )
    book2 = BookRead(
        # id=uuid4(),
        id=UUID("de1288cc-5eb7-42b1-9e66-5a4b9a29a261"),
        title="Bidenbook",
        author="Ggggg",
        price=1333.99
    )
    book3 = BookRead(
        # id=uuid4(),
        id=UUID("634af327-9d9d-49fd-a671-2cef810de932"),
        title="Ddddddd",
        author="Hhhhhh",
        price=14.00
    )
    books[book1.id] = book1
    books[book2.id] = book2
    books[book3.id] = book3

    lib1 = LibraryRead(
        # id=uuid4(),
        id=UUID("7c8f1060-db19-4e6f-b087-2f944c4aede5"),
        code="BUT",
        name="Butler Library"
    )
    lib2 = LibraryRead(
        # id=uuid4(),
        id=UUID("cc8b6202-2568-411a-aa47-e138c7bd0f4e"),
        code="AVY",
        name="Avery Architectural & Fine Arts Library"
    )
    lib3 = LibraryRead(
        # id=uuid4(),
        id=UUID("b8a518f6-c4ff-459d-b5c1-973d1b8b3c7d"),
        code="SEL",
        name="Science & Engineering Library"
    )
    libraries[lib1.id] = lib1
    libraries[lib2.id] = lib2
    libraries[lib3.id] = lib3


    print(f"Book IDs: {list(books.keys())}")
    print(f"Library IDs: {list(libraries.keys())}")

add_data()

app = FastAPI(
    title="Person/Address/Book/Library API",
    description="Demo FastAPI app using Pydantic v2 models for Person, Address, Book, and Library",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    # Each person gets its own UUID; stored as PersonRead
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# -----------------------------------------------------------------------------
# Book endpoints
# -----------------------------------------------------------------------------
@app.post("/books", response_model=BookRead, status_code=201)
def create_book(book: BookCreate):
    book_read = BookRead(**book.model_dump())
    books[book_read.id] = book_read
    return book_read

@app.get("/books", response_model=List[BookRead])
def list_books(
    author: Optional[str] = Query(None, description="Filter by author (exact match)"),
    title_contains: Optional[str] = Query(None, description="Filter by title containing substring"),
    min_price: Optional[float] = Query(None, description="Minimum price filter", ge=0),
    max_price: Optional[float] = Query(None, description="Maximum price filter", ge=0),
    limit: int = Query(10, description="Number of results to return", ge=1, le=20),
    offset: int = Query(0, description="Number of results to skip", ge=0),
):
    results = list(books.values())

    if author is not None:
        results = [b for b in results if b.author is not None and b.author == author]
    if title_contains is not None:
        results = [b for b in results if title_contains.lower() in b.title.lower()]
    if min_price is not None:
        results = [b for b in results if b.price >= min_price]
    if max_price is not None:
        results = [b for b in results if b.price <= max_price]

    return results[offset:offset + limit]

@app.get("/books/{book_id}", response_model=BookRead)
def get_book(
    book_id: UUID = Path(..., description="Book ID"),
    fields: Optional[str] = Query(None, description=" fields to return separated by comma(e.g., 'title,price')"),
):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")

    book = books[book_id]

    if fields is not None:
        field_list = [f.strip() for f in fields.split(',')]
        valid_fields = ['id', 'title', 'author', 'price', 'created_at', 'updated_at']
        result = {}
        for field in field_list:
            if field in valid_fields and hasattr(book, field):
                result[field] = getattr(book, field)
        return result

    return book

@app.patch("/books/{book_id}", response_model=BookRead)
def update_book(book_id: UUID, update: BookUpdate):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    stored = books[book_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    books[book_id] = BookRead(**stored)
    return books[book_id]

@app.put("/books/{book_id}", response_model=BookRead)
def replace_book(book_id: UUID, book: BookReplace):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    book_read = BookRead(id=book_id, **book.model_dump())
    books[book_id] = book_read
    return book_read

@app.delete("/books/{book_id}")
def delete_book(book_id: UUID):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[book_id]
    return {"message": "Book deleted successfully"}

# -----------------------------------------------------------------------------
# Library endpoints
# -----------------------------------------------------------------------------
@app.post("/libraries", response_model=LibraryRead, status_code=201)
def create_library(library: LibraryCreate):
    if library.id in libraries:
        raise HTTPException(status_code=400, detail="Library with this ID already exists")

    for existing_library in libraries.values():
        if existing_library.code.lower() == library.code.lower():
            raise HTTPException(status_code=400, detail="A library with this code already exists")
        if existing_library.name.lower() == library.name.lower():
            raise HTTPException(status_code=400, detail="A library with this name already exists")

    library_read = LibraryRead(**library.model_dump())
    libraries[library_read.id] = library_read
    return library_read

@app.get("/libraries", response_model=List[LibraryRead])
def list_libraries(
    code: Optional[str] = Query(None, description="Filter by code"),
    name: Optional[str] = Query(None, description="Filter by name"),
    name_contains: Optional[str] = Query(None, description="Filter by name containing substring"),
    limit: int = Query(50, description="Number of results to return", ge=1, le=20),
    offset: int = Query(0, description="Number of results to skip", ge=0),
):
    results = list(libraries.values())

    if code is not None:
        results = [l for l in results if l.code.lower() == code.lower()]
    if name is not None:
        results = [l for l in results if l.name.lower() == name.lower()]
    if name_contains is not None:
        results = [l for l in results if name_contains.lower() in l.name.lower()]

    return results[offset:offset + limit]

@app.get("/libraries/{library_id}", response_model=LibraryRead)
def get_library(library_id: UUID):
    if library_id not in libraries:
        raise HTTPException(status_code=404, detail="Library not found")
    return libraries[library_id]

@app.patch("/libraries/{library_id}", response_model=LibraryRead)
def update_library(library_id: UUID, update: LibraryUpdate):
    if library_id not in libraries:
        raise HTTPException(status_code=404, detail="Library not found")
    if update.code is not None or update.name is not None:
        for existing_library in libraries.values():
            if existing_library.id != library_id:
                if update.code is not None and existing_library.code.lower() == update.code.lower():
                    raise HTTPException(status_code=400, detail="A library with this code already exists")
                if update.name is not None and existing_library.name.lower() == update.name.lower():
                    raise HTTPException(status_code=400, detail="A library with this name already exists")

    stored = libraries[library_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    libraries[library_id] = LibraryRead(**stored)
    return libraries[library_id]

@app.put("/libraries/{library_id}", response_model=LibraryRead)
def replace_library(library_id: UUID, library: LibraryReplace):
    if library_id not in libraries:
        raise HTTPException(status_code=404, detail="Library not found")

    for existing_library in libraries.values():
        if existing_library.id != library_id:
            if existing_library.code.lower() == library.code.lower():
                raise HTTPException(status_code=400, detail="A library with this code already exists")
            if existing_library.name.lower() == library.name.lower():
                raise HTTPException(status_code=400, detail="A library with this name already exists")

    library_read = LibraryRead(id=library_id, **library.model_dump())
    libraries[library_id] = library_read
    return library_read

@app.delete("/libraries/{library_id}")
def delete_library(library_id: UUID):
    if library_id not in libraries:
        raise HTTPException(status_code=404, detail="Library not found")
    del libraries[library_id]
    return {"message": "Library deleted successfully"}

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address/Book/Library API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
