from datetime import date

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.evaluation_cycle import EvaluationCycle


def _quarter_dates(year: int):
    return (
        (1, date(year, 1, 1), date(year, 3, 31)),
        (2, date(year, 4, 1), date(year, 6, 30)),
        (3, date(year, 7, 1), date(year, 9, 30)),
        (4, date(year, 10, 1), date(year, 12, 31)),
    )


def ensure_evaluation_cycles(db: Session, year: int):
    for quarter, start_date, end_date in _quarter_dates(year):
        statement = insert(EvaluationCycle).values(
            year=year,
            quarter=quarter,
            start_date=start_date,
            end_date=end_date,
        ).on_conflict_do_nothing(
            index_elements=["year", "quarter"]
        )
        db.execute(statement)

    db.commit()

    return (
        db.query(EvaluationCycle)
        .filter(EvaluationCycle.year == year)
        .order_by(EvaluationCycle.quarter)
        .all()
    )


def get_current_evaluation_cycle(
    db: Session,
    current_date: date | None = None,
):
    today = current_date or date.today()

    return (
        db.query(EvaluationCycle)
        .filter(
            EvaluationCycle.start_date <= today,
            EvaluationCycle.end_date >= today,
        )
        .first()
    )