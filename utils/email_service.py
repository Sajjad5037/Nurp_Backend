import os

from datetime import date, timedelta

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

FROM_EMAIL = "noreply@gemkidsacademy.com.au"

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)
print("FRONTEND_URL =", FRONTEND_URL)

NURP_LOGO_URL = f"{FRONTEND_URL}/nurp-logo.png"


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

    access_token: str,

    workflow_type: str = "employee_evaluation",

    evaluation_cycle_year: int | None = None,

    evaluation_cycle_quarter: int | None = None

):

    evaluation_link = (
        f"{FRONTEND_URL}/evaluation/{access_token}"
    )

    if workflow_type == "goal_kpi_setting":

        quarter_label = (
            f"Q{evaluation_cycle_quarter} {evaluation_cycle_year}"
            if evaluation_cycle_quarter and evaluation_cycle_year
            else "the upcoming cycle"
        )

        deadline_label = (
            date.today() + timedelta(days=3)
        ).strftime("%B %d, %Y")

        html = f"""
        <html>

        <body style="font-family:Arial">

            <p>
                <img src="{NURP_LOGO_URL}" alt="Nurp" style="max-height:60px;">
            </p>

            <h2>Hello {employee_name},</h2>

            <p>
                You have been assigned your Goal & KPI form for the
                upcoming {quarter_label}.
            </p>

            <p>
                This evaluation is designed to align your individual
                objectives with Nurp's strategic goals and ensure you
                have a clear, measurable roadmap for success.
            </p>

            <p>
                To help you complete this form effectively, here is a
                brief explanation of each section:
            </p>

            <ul>

                <li>
                    Goals: Your top priorities to drive the most value
                    for the business over the next 3 months.
                </li>

                <li>
                    KPIs (Key Performance Indicators): Measurable
                    metrics that represent output and can be tracked
                    at least on a weekly or monthly basis.
                </li>

            </ul>

            <p>
                Please click the button below to begin.
            </p>

            <p style="margin: 24px 0;">

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
                Once you submit your entries, you will have the
                opportunity to discuss and finalize these goals during
                the upcoming HR meeting.
            </p>

            <p>
                Please complete your portion of the form by
                {deadline_label}. If you have any questions regarding
                the goals or the platform, please reach out to the HR
                team.
            </p>

            <br>

            <p>

                Regards,

                <br>

                Nurp Talent Managment Team

            </p>

        </body>

        </html>
        """

        return send_email(

            to_email=employee_email,

            subject=(
                f"Action Required: Your Goal & KPI Form for "
                f"{quarter_label} - Nurp"
            ),

            html=html

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

    access_token: str,

    workflow_type: str = "employee_evaluation",

    evaluation_cycle_year: int | None = None,

    evaluation_cycle_quarter: int | None = None

):

    evaluation_link = (
        f"{FRONTEND_URL}/evaluation/{access_token}"
    )

    if workflow_type == "goal_kpi_setting":

        quarter_label = (
            f"Q{evaluation_cycle_quarter} {evaluation_cycle_year}"
            if evaluation_cycle_quarter and evaluation_cycle_year
            else "the upcoming cycle"
        )

        deadline_label = (
            date.today() + timedelta(days=3)
        ).strftime("%B %d, %Y")

        html = f"""
        <html>

        <body style="font-family:Arial">

            <p>
                <img src="{NURP_LOGO_URL}" alt="Nurp" style="max-height:60px;">
            </p>

            <h2>Hi {supervisor_name},</h2>

            <p>
                This is a notification that {employee_name} has been
                assigned their Goal & KPI form for the upcoming
                {quarter_label}.
            </p>

            <p>
                As their supervisor, you are required to independently
                complete your own Goal & KPI sheet for this employee,
                outlining what you believe should be their top
                priorities.
            </p>

            <p>
                To help you complete this form effectively, here is a
                brief reminder of the structure:
            </p>

            <ul>

                <li>
                    Goals: The top priorities to drive the most value
                    for the business over the next 3 months.
                </li>

                <li>
                    KPIs: Measurable metrics that represent output and
                    can be tracked at least on a weekly or monthly
                    basis.
                </li>

            </ul>

            <p>
                Please click the button below to access the evaluation
                platform and submit your entries.
            </p>

            <p style="margin: 24px 0;">

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
                You will have the opportunity to discuss and finalize
                these together with the employee during the upcoming
                HR meeting.
            </p>

            <p>
                Kindly complete your independent submission by
                {deadline_label} so HR can prepare for the finalization
                meeting. If you need any support navigating the
                platform, please contact HR.
            </p>

            <br>

            <p>

                Regards,

                <br>

                Nurp Talent Management Team

            </p>

        </body>

        </html>
        """

        return send_email(

            to_email=supervisor_email,

            subject=(
                f"Action Required: Goal & KPI Sheet for "
                f"{employee_name} - Nurp"
            ),

            html=html

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
    supervisor_name: str,
    access_token: str,
    quarter_year: str,
    deadline: str = None,
):
    evaluation_link = (
        f"{FRONTEND_URL}/evaluation/{access_token}"
    )

    logo_url = f"{FRONTEND_URL}/nurp-logo.png"

    html = f"""
    <html>

    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">

        <div style="max-width: 650px; margin: 0 auto;">

            <!-- Nurp Logo -->
            <div style="margin-bottom: 30px;">
                <img
                    src="{logo_url}"
                    alt="Nurp"
                    style="max-width: 180px; height: auto;"
                >
            </div>

            <h2>Hi {hr_name},</h2>

            <p>
                This is an automated notification to inform you that the
                Goal &amp; KPI forms have been filled by both
                <strong>{employee_name}</strong> and their supervisor,
                <strong>{supervisor_name}</strong>, for the upcoming
                <strong>{quarter_year}</strong>.
            </p>

            <p>
                Both parties have been asked to independently submit their
                goals and KPIs. You can track the progress and completion
                status of both submissions by clicking the button below.
            </p>

            <p style="margin: 30px 0;">
                <a
                    href="{evaluation_link}"
                    style="
                        background:#1976d2;
                        color:white;
                        padding:12px 20px;
                        text-decoration:none;
                        border-radius:6px;
                        display:inline-block;
                    "
                >
                    Track Evaluation
                </a>
            </p>

            <p>
                Please monitor the submission progress. Once both parties
                have submitted, please schedule the HR finalization meeting
                to align and lock in the final goals and KPIs.
            </p>

            <br>

            <p>
                Regards,<br>
                <strong>Nurp Talent Management Team</strong>
            </p>

        </div>

    </body>

    </html>
    """

    return send_email(
        to_email=hr_email,
        subject=f"Notification: Goal & KPI Forms Assigned to {employee_name} - Nurp",
        html=html
    )