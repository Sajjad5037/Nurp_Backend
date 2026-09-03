from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates" / "pdf"


def generate_master_sheet_pdf(master_sheet):
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR))
    )

    template = env.get_template(
        "evaluation_master_sheet.html"
    )
    company_information = next(
        (
            component
            for component in (
                master_sheet.get("workflow_json", {})
                .get("stages", {})
                .get("employee", [])
            )
            if component.get("id") == "company_information"
        ),
        {}
    )

    employee_goals_planning = (
        (master_sheet.get("employee_responses") or {})
        .get("q3_goals_planning", {})
    )
    supervisor_goals_planning = (
        (master_sheet.get("supervisor_responses") or {})
        .get("q3_goals_planning", {})
    )
    hr_goals_planning = (
        (master_sheet.get("hr_responses") or {})
        .get("q3_goals_planning", {})
    )

    employee_goals = employee_goals_planning.get("employee_goals", [])
    supervisor_goals = supervisor_goals_planning.get("supervisor_goals", [])
    hr_final_goals = hr_goals_planning.get("hr_final_goals", [])
    employee_ratings = employee_goals_planning.get(
        "employee_rating_by_goal", {}
    )
    supervisor_ratings = supervisor_goals_planning.get(
        "supervisor_rating_by_goal", {}
    )
    final_ratings = hr_goals_planning.get("final_rating_by_goal", {})

    quarterly_goals = []
    q3_goals_planning = []

    goal_count = max(len(employee_goals), len(supervisor_goals))
    for index in range(goal_count):
        employee_goal = employee_goals[index] if index < len(employee_goals) else {}
        supervisor_goal = (
            supervisor_goals[index] if index < len(supervisor_goals) else {}
        )
        employee_goal_id = employee_goal.get("id")
        goal_id = employee_goal_id or supervisor_goal.get("id")
        hr_final_goal = next(
            (
                goal
                for goal in hr_final_goals
                if goal.get("goalId") == employee_goal_id
            ),
            {}
        )

        quarterly_goals.append({
            "id": goal_id,
            "description": (
                hr_final_goal.get("finalGoal")
                or employee_goal.get("description")
                or supervisor_goal.get("description")
                or ""
            ),
            "employee_response": employee_goal.get("description", ""),
            "supervisor_response": supervisor_goal.get("description", ""),
            "final_goal": hr_final_goal.get("finalGoal", ""),
            "employee_rating": employee_ratings.get(goal_id),
            "supervisor_rating": supervisor_ratings.get(goal_id),
            "final_rating": final_ratings.get(goal_id),
            "monthly_progress": {},
            "completion_date": "",
        })

        q3_goals_planning.append({
            "id": goal_id,
            "goal_number": index + 1,
            "employee_response": employee_goal.get("description", ""),
            "supervisor_response": supervisor_goal.get("description", ""),
            "final_goal": hr_final_goal.get("finalGoal", ""),
        })

    quarterly_goal_months = master_sheet.get("review_cycle_months", [])

    employee_kpi_results = (
        (master_sheet.get("employee_responses") or {})
        .get("kpi_results", {})
    )
    supervisor_kpi_results = (
        (master_sheet.get("supervisor_responses") or {})
        .get("kpi_results", {})
    )
    hr_responses = master_sheet.get("hr_responses") or {}
    hr_kpi_results = hr_responses.get("kpi_results", {})
    finalized_kpis = master_sheet.get("finalized_kpis", [])

    quarterly_kpis = []
    for kpi in finalized_kpis:
        kpi_id = kpi.get("id")
        kpi_result = hr_kpi_results.get(str(kpi_id), {})

        quarterly_kpis.append({
            "id": kpi_id,
            "title": kpi.get("title"),
            "expectation": kpi.get("expectation"),
            "july": kpi_result.get("july"),
            "august": kpi_result.get("august"),
            "september": kpi_result.get("september"),
            "q3_average": kpi_result.get("q3_average"),
            "comments": kpi_result.get("comments", ""),
        })

    kpi_employee_rating = employee_kpi_results.get("overall_rating")
    kpi_supervisor_rating = supervisor_kpi_results.get("overall_rating")
    kpi_final_rating = hr_kpi_results.get("overall_rating")
    kpi_section_points = hr_kpi_results.get("section_points", "")

    employee_kpi_proposals = (
        (master_sheet.get("employee_responses") or {})
        .get("kpi_review_planning", {})
        .get("employee_proposals", [])
    )
    supervisor_kpi_proposals = (
        (master_sheet.get("supervisor_responses") or {})
        .get("kpi_review_planning", {})
        .get("supervisor_proposals", [])
    )
    hr_final_agreed_kpis = (
        hr_responses
        .get("kpi_review_planning", {})
        .get("final_agreed_kpis", [])
    )

    q4_kpi_planning = []
    for index, finalized_kpi in enumerate(finalized_kpis):
        employee_proposal = (
            employee_kpi_proposals[index]
            if index < len(employee_kpi_proposals)
            else {}
        )
        supervisor_proposal = (
            supervisor_kpi_proposals[index]
            if index < len(supervisor_kpi_proposals)
            else {}
        )

        q4_kpi_planning.append({
            "current_title": finalized_kpi.get("title"),
            "current_expectation": finalized_kpi.get("expectation"),
            "employee_suggestion": employee_proposal.get("title"),
            "employee_expectation": employee_proposal.get("proposed"),
            "supervisor_suggestion": supervisor_proposal.get("title"),
            "supervisor_expectation": supervisor_proposal.get("proposed"),
        })

    q4_final_kpis = [
        {
            "title": kpi.get("title"),
            "expectation": kpi.get("expectation"),
        }
        for kpi in finalized_kpis
    ]

    hr_extra_projects = (
        (master_sheet.get("hr_responses") or {})
        .get("hr_extra_projects", [])
    )

    extra_projects = [
        {
            "description": project.get("description"),
            "start_date": project.get("startDate"),
            "end_date": project.get("endDate"),
        }
        for project in hr_extra_projects
    ]

    print("PDF extra_projects:", extra_projects)

    discussion_notes_feedback = (
        (master_sheet.get("employee_responses") or {})
        .get("discussion_notes_feedback", {})
    )

    supervisor_discussion_notes_feedback = (
        (master_sheet.get("supervisor_responses") or {})
        .get("discussion_notes_feedback", {})
    )

    employee_discussion_response = discussion_notes_feedback.get(
        "employee_response",
        "",
    )

    supervisor_discussion_response = supervisor_discussion_notes_feedback.get(
        "supervisor_response",
        "",
    )
    q4_feedback_employee = (
        (master_sheet.get("employee_responses") or {})
        .get("q3_feedback_proposed_goals", {})
    )

    q4_feedback_supervisor = (
        (master_sheet.get("supervisor_responses") or {})
        .get("q3_feedback_proposed_goals", {})
    )

    q4_feedback_question1_employee = q4_feedback_employee.get(
        "question1",
        "",
    )

    q4_feedback_question1_supervisor = q4_feedback_supervisor.get(
        "supervisor_question1",
        "",
    )

    q4_feedback_question2_employee = q4_feedback_employee.get(
        "question2",
        "",
    )

    q4_feedback_question2_supervisor = q4_feedback_supervisor.get(
        "supervisor_question2",
        "",
    )

    performance_and_core_values = (
        (master_sheet.get("supervisor_responses") or {})
        .get("performance_and_core_values", {})
    )

    professional_attributes_response = performance_and_core_values.get(
        "professional_attributes",
        "",
    )

    core_values_response = performance_and_core_values.get(
        "core_values",
        "",
    )




    html = template.render(
        employee_name=master_sheet.get("employee_name"),
        employee_email=master_sheet.get("employee_email"),
        designation=master_sheet.get("designation"),
        department=master_sheet.get("department"),
        supervisor_name=master_sheet.get("supervisor_name"),
        supervisor_email=master_sheet.get("supervisor_email"),
        review_cycle=master_sheet.get("review_cycle"),
        status=master_sheet.get("status"),
        workflow_type=master_sheet.get("workflow_type"),
        workflow_json=master_sheet.get("workflow_json"),
        company_information=company_information,
        company_mission=company_information.get("mission"),
        company_core_values=company_information.get("coreValues", []),
        company_rating_guide=company_information.get("ratingGuide", []),
        company_show_mission=company_information.get("showMission", True),
        company_show_core_values=company_information.get("showCoreValues", True),
        quarterly_goals=quarterly_goals,
        q3_goals_planning=q3_goals_planning,
        quarterly_goal_months=quarterly_goal_months,
        quarterly_kpis=quarterly_kpis,
        kpi_employee_rating=kpi_employee_rating,
        kpi_supervisor_rating=kpi_supervisor_rating,
        kpi_final_rating=kpi_final_rating,
        kpi_section_points=kpi_section_points,
        q4_kpi_planning=q4_kpi_planning,
        q4_final_kpis=q4_final_kpis,
        extra_projects=extra_projects,
        employee_discussion_response=employee_discussion_response,
        supervisor_discussion_response=supervisor_discussion_response,
        q4_feedback_question1_employee=q4_feedback_question1_employee,
        q4_feedback_question1_supervisor=q4_feedback_question1_supervisor,
        q4_feedback_question2_employee=q4_feedback_question2_employee,
        q4_feedback_question2_supervisor=q4_feedback_question2_supervisor,
        professional_attributes_response=professional_attributes_response,
        core_values_response=core_values_response,
    )

    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page()

        page.set_content(html)

        pdf_bytes = page.pdf(
            format="A4",
            landscape=True,
            print_background=True,
            margin={
                "top": "10mm",
                "right": "10mm",
                "bottom": "10mm",
                "left": "10mm",
            },
        )

        browser.close()

        return pdf_bytes


# Temporary test function.
# Keep this until the real PDF endpoint is verified.
def generate_test_pdf():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page()

        page.set_content("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @page {
                    size: A4 landscape;
                    margin: 10mm;
                }

                body {
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                }

                h1 {
                    font-size: 22px;
                }
            </style>
        </head>

        <body>
            <h1>FlowPilot PDF Test</h1>

            <p>
                This is a test PDF generated using Playwright and Chromium.
            </p>
        </body>
        </html>
        """)

        pdf_bytes = page.pdf(
            format="A4",
            landscape=True,
            margin={
                "top": "10mm",
                "right": "10mm",
                "bottom": "10mm",
                "left": "10mm",
            },
        )

        browser.close()

        return pdf_bytes