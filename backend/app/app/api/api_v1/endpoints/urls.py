from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from app.api.deps import SessionDep
from app.models import URL, URLCreate, URLRead
from app.crud.crud_urls import (
    create_db_url,
    deactivate_db_url_by_secret_key,
    get_db_url_by_key,
    get_db_url_by_secret_key,
    get_admin_info,
    update_db_clicks
)

router = APIRouter()


@router.post("/urls")
def create_url(db: SessionDep, url: URLCreate):
    db_url = create_db_url(db=db, url=url)
    return db_url


@router.get("/{url_key}")
def read_url(
        url_key: str,
        request: Request,
        db: SessionDep
):
    if db_url := get_db_url_by_key(db=db, url_key=url_key):
        update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"URL '{request.url}' doesn't exist."
        )


@router.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=URLRead
)
def read_url_info(
    secret_key: str, request: Request, db: SessionDep
):
    if db_url := get_db_url_by_secret_key(db=db, secret_key=secret_key):
        return get_admin_info(db_url)

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"URL '{request.url}' doesn't exist."
        )


@router.delete("/admin/{secret_key}")
def delete_url(
        secret_key: str, request: Request, db: SessionDep
):
    if db_url := deactivate_db_url_by_secret_key(db=db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"URL '{request.url}' doesn't exist."
        )
