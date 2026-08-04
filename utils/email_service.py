import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

FROM_EMAIL = "noreply@gemkidsacademy.com.au"

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)
print("FRONTEND_URL =", FRONTEND_URL)


# --------------------------------------------------
# Generic Email Sender
# --------------------------------------------------

def send_email(
    to_email: str,
    subject: str,
    html: str
):

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html
    )

    try:

        sg = SendGridAPIClient(SENDGRID_API_KEY)

        response = sg.send(message)

        print(
            f"[INFO] Email sent successfully "
            f"({response.status_code})"
        )

        return True

    except Exception as e:

        print(f"[ERROR] {e}")

        return False


# --------------------------------------------------
# Employee Evaluation Email
# --------------------------------------------------

def send_employee_evaluation_email(

    employee_name: str,

    employee_email: str,

    access_token: str

):

    evaluation_link = (
        f"{FRONTEND_URL}/evaluation/{access_token}"
    )

    html = f"""
    <html>

    <body style="font-family:Arial">

        <h2>Hello {employee_name},</h2>

        <p>
            You have been assigned a new performance evaluation.
        </p>

        <p>
            Please click the button below to begin.
        </p>

        <p>

            <a
                href="{evaluation_link}"
                style="
                    background:#1976d2;
                    color:white;
                    padding:12px 20px;
                    text-decoration:none;
                    border-radius:6px;
                "
            >

                Start Evaluation

            </a>

        </p>

        <p>
            If the button does not work, use this link:
        </p>

        <p>

            <a href="{evaluation_link}">
                {evaluation_link}
            </a>

        </p>

        <br>

        <p>

            Regards,

            <br>

            FlowPilot

        </p>

    </body>

    </html>
    """

    return send_email(

        to_email=employee_email,

        subject="Performance Evaluation Assigned",

        html=html

    )


# --------------------------------------------------
# Supervisor Email
# --------------------------------------------------

def send_supervisor_evaluation_email(

    supervisor_name: str,

    supervisor_email: str,

    employee_name: str,

    access_token: str

):

    evaluation_link = (
        f"{FRONTEND_URL}/evaluation/{access_token}"
    )

    html = f"""
    <html>

    <body style="font-family:Arial">

        <h2>Hello {supervisor_name},</h2>

        <p>
            {employee_name} has completed their self evaluation.
        </p>

        <p>
            Please complete your supervisor review.
        </p>

        <p>

            <a
                href="{evaluation_link}"
                style="
                    background:#1976d2;
                    color:white;
                    padding:12px 20px;
                    text-decoration:none;
                    border-radius:6px;
                "
            >

                Open Evaluation

            </a>

        </p>

    </body>

    </html>
    """

    return send_email(

        to_email=supervisor_email,

        subject="Employee Evaluation Ready For Review",

        html=html

    )


# --------------------------------------------------
# HR Email
# --------------------------------------------------

def send_hr_evaluation_email(

    hr_name: str,

    hr_email: str,

    employee_name: str,

    access_token: str

):

    evaluation_link = (
        f"{FRONTEND_URL}/evaluation/{access_token}"
    )

    html = f"""
    <html>

    <body style="font-family:Arial">

        <h2>Hello {hr_name},</h2>

        <p>
            The supervisor has completed the evaluation for
            <b>{employee_name}</b>.
        </p>

        <p>
            Please complete the HR review.
        </p>

        <p>

            <a
                href="{evaluation_link}"
                style="
                    background:#1976d2;
                    color:white;
                    padding:12px 20px;
                    text-decoration:none;
                    border-radius:6px;
                "
            >

                Open Evaluation

            </a>

        </p>

    </body>

    </html>
    """

    return send_email(

        to_email=hr_email,

        subject="Evaluation Ready For HR Review",

        html=html

    )