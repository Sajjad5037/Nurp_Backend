from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.employee import Employee
from schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# --------------------------------------------------
# Create Employee
# --------------------------------------------------

@router.post(
    "",
    response_model=EmployeeResponse
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    print("==============================================")
    print("CREATE EMPLOYEE DEBUG")
    print("==============================================")
    print("POST /employees received")
    print("full_name:", employee.full_name)
    print("email:", employee.email)
    print("is_active:", getattr(employee, "is_active", None))

    print("Checking for existing employee with email and role:", employee.email, employee.role)

    existing = (
        db.query(Employee)
        .filter(Employee.email == employee.email)
        .filter(Employee.role == employee.role)
        .first()
    )

    print("Existing employee found:", existing is not None)
    if existing:
        print("existing.id:", existing.id)
        print("existing.full_name:", existing.full_name)
        print("existing.email:", existing.email)
        print("existing.is_active:", existing.is_active)

    if existing:
        print("CREATE EMPLOYEE REJECTED: duplicate email and role")
        print("existing employee id:", existing.id)
        print("existing employee email:", existing.email)
        print("existing employee is_active:", existing.is_active)
        raise HTTPException(
            status_code=400,
            detail="Employee with this email and role already exists."
        )

    print("CREATING NEW EMPLOYEE")
    print("email:", employee.email)
    print("is_active:", getattr(employee, "is_active", None))

    db_employee = Employee(
        full_name=employee.full_name,
        email=employee.email,
        slack_id=employee.slack_id,
        department=employee.department,
        designation=employee.designation,
        role=employee.role
    )

    db.add(db_employee)

    try:
        db.commit()
    except Exception as e:
        print("CREATE EMPLOYEE COMMIT FAILED")
        print("exception:", repr(e))
        raise

    db.refresh(db_employee)

    print("CREATE EMPLOYEE SUCCESS")
    print("created employee id:", db_employee.id)
    print("email:", db_employee.email)
    print("is_active:", db_employee.is_active)

    return db_employee


# --------------------------------------------------
# Get All Employees
# --------------------------------------------------

@router.get(
    "",
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):

    return (
        db.query(Employee)
        .order_by(Employee.full_name)
        .all()
    )


# --------------------------------------------------
# Get Single Employee
# --------------------------------------------------

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    return employee


# --------------------------------------------------
# Update Employee
# --------------------------------------------------

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    db_employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not db_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    db_employee.full_name = employee.full_name
    db_employee.email = employee.email
    db_employee.slack_id = employee.slack_id
    db_employee.department = employee.department
    db_employee.designation = employee.designation
    db_employee.role = employee.role
    db_employee.is_active = employee.is_active

    db.commit()
    db.refresh(db_employee)

    return db_employee


# --------------------------------------------------
# Delete Employee
# --------------------------------------------------

@router.delete(
    "/{employee_id}"
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully."
    }