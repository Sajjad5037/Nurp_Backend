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

        html = f"""
        <html>

        <body style="font-family:Arial; line-height:1.6; color:#333;">

            <p>
                <img src="{NURP_LOGO_URL}" alt="Nurp" style="max-height:60px;">
            </p>

            <h2>Hello {employee_name},</h2>

            <p>
                You have been assigned your Goal &amp; KPI form for the
                upcoming {quarter_label}.
            </p>

            <p>
                This evaluation is designed to align your individual
                objectives with Nurp's strategic goals and ensure you
                have a clear, measurable roadmap for success.
            </p>

            <p>
                To help you complete the form effectively, here is a
                brief explanation of each section:
            </p>

            <ul>

                <li>
                    <strong>Goals:</strong> Your top priorities to drive
                    the most value for the business over the next 3
                    months.
                </li>

                <li>
                    <strong>KPIs (Key Performance Indicators):</strong>
                    Measurable metrics that represent output and can be
                    tracked at least on a weekly or monthly basis.
                </li>

            </ul>

            <p>
                We have also prepared a brief video guide that walks you
                through how to complete the Goal &amp; KPI form. Please
                review the guide before submitting your entries:
            </p>

            <p>
                <a href="https://atlas.nurp.com/goal-kpi-filling-tutorial">
                    Watch the Goal &amp; KPI Form Guide
                </a>
            </p>

            <p>
                Once you are ready, please click the button below to
                begin:
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
                        display:inline-block;
                    "
                >
                    Start Goal &amp; KPI form
                </a>
            </p>

            <p>
                Once you submit your entries, you will have the
                opportunity to discuss and finalize these goals during
                the upcoming HR meeting.
            </p>

            <p>
                Please complete your portion of the form by [Date +3
                days]. If you have any questions regarding the goals or
                the platform, please reach out to the HR team.
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

            to_email=employee_email,

            subject=(
                f"Action Required: Your Goal & KPI Form for {quarter_label} - Nurp"
            ),

            html=html

        )

    quarter_label = (
        f"Q{evaluation_cycle_quarter} {evaluation_cycle_year}"
        if evaluation_cycle_quarter and evaluation_cycle_year
        else "the upcoming cycle"
    )

    html = f"""
    <html>

    <body style="font-family:Arial; line-height:1.6; color:#333;">

        <p>
            <img src="{NURP_LOGO_URL}" alt="Nurp" style="max-height:60px;">
        </p>

        <h2>Hello {employee_name},</h2>

        <p>
            Following your recent HR meeting, your Goal &amp; KPI
            evaluation for {quarter_label} has been finalized, with
            your goals, KPIs, and targets assigned for the upcoming
            quarter.
        </p>

        <p>
            You can revisit your evaluation at any time throughout the
            quarter to review your progress and see how you are tracking
            against your targets. All goals and KPIs are tracked monthly
            by your supervisor, allowing you to monitor your progress and
            stay aligned with the expectations established during your HR
            meeting.
        </p>

        <p>
            Please keep the following in mind:
        </p>

        <ul>

            <li>
                <strong>Monthly Progress Tracking:</strong> Your
                supervisor will update your progress against each goal
                and KPI on a monthly basis.
            </li>

            <li>
                <strong>Access to Your Results:</strong> All entries and
                progress updates will be visible in both your employee
                evaluation form and your supervisor's evaluation form.
            </li>

            <li>
                <strong>Ongoing Review:</strong> We encourage you to
                revisit your evaluation each month to review your
                results, identify areas that may need attention, and stay
                focused on your targets for the quarter.
            </li>

        </ul>

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
            Your evaluation will serve as a reference point throughout
            the quarter, helping ensure clarity, accountability, and
            alignment between you and your supervisor.
        </p>

        <p>
            If you have any questions regarding your goals, KPIs, or
            evaluation form, please reach out to the HR team.
        </p>

        <p>
            <a href="https://atlas.nurp.com/employee-evaluation-tutorials">
                Watch the Evaluation Form Guide here.
            </a>
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

        to_email=employee_email,

        subject=f"Evaluation form for {quarter_label} is Finalized | Nurp",

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

        html = f"""
        <html>

        <body style="font-family:Arial; line-height:1.6; color:#333;">

            <p>
                <img src="{NURP_LOGO_URL}" alt="Nurp" style="max-height:60px;">
            </p>

            <h2>Hi {supervisor_name},</h2>

            <p>
                This is a notification that {employee_name} has been
                assigned their Goal &amp; KPI form for the upcoming
                {quarter_label}.
            </p>

            <p>
                As their supervisor, you are required to independently
                complete your own Goal &amp; KPI sheet for this employee,
                outlining what you believe should be their top
                priorities.
            </p>

            <p>
                To help you complete this form effectively, here is a
                brief reminder of the structure:
            </p>

            <ul>

                <li>
                    <strong>Goals:</strong> The top priorities to drive
                    the most value for the business over the next 3
                    months.
                </li>

                <li>
                    <strong>KPIs:</strong> Measurable metrics that
                    represent output and can be tracked at least on a
                    weekly or monthly basis.
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
                        display:inline-block;
                    "
                >
                    Start Goal &amp; KPI form
                </a>
            </p>

            <p>
                You will have the opportunity to discuss and finalize
                these together with the employee during the upcoming HR
                meeting.
            </p>

            <p>
                Kindly complete your independent submission by (Date +3
                days) so HR can prepare for the finalization meeting. If
                you need any support navigating the platform, please
                contact HR.
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
                f"Action Required: Goal & KPI Sheet for {employee_name} - Nurp"
            ),

            html=html

        )

    quarter_label = (
        f"Q{evaluation_cycle_quarter} {evaluation_cycle_year}"
        if evaluation_cycle_quarter and evaluation_cycle_year
        else "the upcoming cycle"
    )

    html = f"""
    <html>

    <body style="font-family:Arial; line-height:1.6; color:#333;">

        <p>
            <img src="{NURP_LOGO_URL}" alt="Nurp" style="max-height:60px;">
        </p>

        <h2>Hello {supervisor_name},</h2>

        <p>
            Following the HR meeting, the Goals and KPIs for your team
            members for the upcoming {quarter_label} have been finalized
            and assigned.
        </p>

        <p>
            Each month, HR will update the master evaluation sheet with
            the progress and results provided by you. This information
            will then be reflected in both the employee's evaluation form
            and your supervisor evaluation form, allowing both you and the
            employee to review the same information and track progress
            throughout the quarter.
        </p>

        <p>
            Please provide HR with the following information for each
            team member on a monthly basis:
        </p>

        <ul>

            <li>
                <strong>Goal Progress:</strong> Progress made toward each
                assigned goal.
            </li>

            <li>
                <strong>KPI Results:</strong> Actual results for each
                assigned KPI compared with the established target.
            </li>

            <li>
                <strong>Progress Notes:</strong> Any relevant context,
                achievements, challenges, or changes that should be
                documented.
            </li>

        </ul>

        <p>
            The purpose of the monthly update is to maintain an accurate
            record of performance throughout the quarter rather than
            relying solely on the final evaluation. Employees will be
            able to review their progress, while supervisors can use the
            information to guide ongoing performance discussions and
            accountability.
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
                            HR will handle entering the information into the master sheet
                            and ensuring the updated data is reflected in both evaluation
                            forms.
                        </p>

                        <p>
                            If you have any questions regarding the process or the
                            information required, please reach out to the HR team.
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
            f"Evaluation form for {employee_name} {quarter_label} is Finalized | Nurp"
        ),

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
    workflow_type: str = "employee_evaluation",
):
    evaluation_link = (
        f"{FRONTEND_URL}/evaluation/{access_token}"
    )

    logo_url = f"{FRONTEND_URL}/nurp-logo.png"

    if workflow_type == "goal_kpi_setting":

        reviewer_name = hr_name
        quarter_label = quarter_year

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

                <h2>Hi {reviewer_name},</h2>

                <p>
                    This is an automated notification to inform you that
                    the Goal &amp; KPI forms have been filled by both
                    <strong>{employee_name}</strong> and their supervisor,
                    <strong>{supervisor_name}</strong>, for the upcoming
                    <strong>{quarter_year}</strong>.
                </p>

                <p>
                    Both parties have been asked to independently submit
                    their goals and KPIs. You can track the progress and
                    completion status of both submissions by clicking the
                    button below.
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
                            display:inline-block;
                        "
                    >
                        Goal &amp; KPI Finalization
                    </a>
                </p>

                <p>
                    Please monitor the submission progress. Once both
                    parties have submitted, please schedule the HR
                    finalization meeting to align and lock in the final
                    goals and KPIs.
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
            subject=(
                f"Notification: Goal & KPI Forms Assigned to {employee_name} - Nurp"
            ),
            html=html
        )

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

            <h2>Hello {hr_name},</h2>

            <p>
                Following the completion of the HR meetings, all employee
                Goals and KPIs for the upcoming {quarter_year} have been
                finalized and assigned.
            </p>

            <p>
                HR will be responsible for maintaining the monthly
                performance records and ensuring that all updates are
                accurately entered into the master evaluation sheet.
            </p>

            <p>
                Each month, HR will collect the Goal and KPI results
                provided by supervisors and enter the information into the
                master sheet. Once updated, the information will be
                reflected in both the employee's evaluation form and the
                supervisor's evaluation form.
            </p>

            <p>
                The monthly process will include:
            </p>

            <ul>

                <li>
                    <strong>Collect Supervisor Updates:</strong> Obtain
                    the monthly Goal and KPI results for each employee
                    from their assigned supervisor.
                </li>

                <li>
                    <strong>Update the Master Sheet:</strong> Enter the
                    reported results, progress, and relevant notes into
                    the appropriate employee records.
                </li>

                <li>
                    <strong>Maintain Accuracy:</strong> Ensure that the
                    information entered matches the goals, KPIs, targets,
                    and tracking criteria established during the HR
                    meeting.
                </li>

                <li>
                    <strong>Maintain Visibility:</strong> Confirm that the
                    updated information is reflected in both the employee
                    and supervisor evaluation forms.
                </li>

                <li>
                    <strong>Track Monthly Progress:</strong> Maintain a
                    complete record of each employee's progress throughout
                    the quarter so that performance can be reviewed based
                    on the full quarter rather than only the final results.
                </li>

                <li>
                    <strong>Prepare for Quarterly Review:</strong> Ensure
                    all monthly updates are completed and organized for
                    the next quarterly evaluation and HR meeting.
                </li>

            </ul>

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
                    Start Evaluation
                </a>
            </p>

            <p>
                Please ensure that all monthly updates are entered
                accurately and in a timely manner so employees and
                supervisors have an up to date view of progress throughout
                the quarter.
            </p>

            <p>
                If there are any discrepancies, missing information, or
                questions regarding a Goal or KPI, please clarify them with
                the appropriate supervisor before finalizing the monthly
                entry.
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
        subject=(
            f"Evaluation form for {employee_name} {quarter_year} is Finalized | Nurp"
        ),
        html=html
    )