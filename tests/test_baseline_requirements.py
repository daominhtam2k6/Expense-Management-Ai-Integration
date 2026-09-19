"""Regression checks for approved AC-018/019, using isolated in-memory data."""
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models.user import User
from app.routers.categories import create_category
from app.schemas.category import CategoryCreate
from app.schemas.budget import BudgetCreate


@pytest.mark.parametrize("year", [1999, 2101])
def test_ac019_rejects_out_of_range_budget_year(year):
    with pytest.raises(ValidationError):
        BudgetCreate(category_id="food", month=9, year=year, limit_amount="100")


@pytest.mark.parametrize("year", [2000, 2100])
def test_ac019_accepts_boundary_budget_year(year):
    assert BudgetCreate(category_id="food", month=9, year=year, limit_amount="100").year == year


@pytest.mark.parametrize("duplicate", ["food", " Food "])
def test_ac018_rejects_normalized_duplicate_category(duplicate):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as db:
            user = User(id="baseline-owner", username="baseline-owner",
                        email="baseline@example.com", password_hash="test-only")
            db.add(user)
            db.commit()
            create_category(CategoryCreate(name="Food", type="expense"), db, user)
            with pytest.raises(HTTPException) as error:
                create_category(CategoryCreate(name=duplicate, type="expense"), db, user)
            assert error.value.status_code in (400, 409)
    finally:
        engine.dispose()
