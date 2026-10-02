import asyncio
import os

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.requirement_reader import load_requirements
from agents.playwright_agent import run_all_playwright_tests
from agents.result_agent import generate_result_summary
from agents.report_agent import write_execution_report


load_dotenv()


async def run_test_automation():

    print()
    print("==================================================")
    print("AI MULTI-AGENT TEST AUTOMATION")
    print("==================================================")
    print()

    # ------------------------------------------------
    # STEP 1 - LOAD REQUIREMENTS
    # ------------------------------------------------

    print("STEP 1: Loading requirements from Excel...")

    requirements = load_requirements()

    print(
        f"Requirements loaded: {len(requirements)}"
    )

    print()

    # ------------------------------------------------
    # STEP 2 - TEST MANAGER AGENT
    # ------------------------------------------------

    print("STEP 2: Test Manager Agent")

    model = os.getenv(
        "OPENAI_MODEL",
        "gpt-4o-mini"
    )

    model_client = OpenAIChatCompletionClient(
        model=model
    )

    test_manager = AssistantAgent(
        name="TestManager",
        model_client=model_client,
        system_message="""
You are the Test Manager Agent in an
AI-powered test automation framework.

Your responsibility is to review the test
requirements supplied by the Requirement Reader.

Do not modify test data.

Do not invent test cases.

Do not execute tests.

Validate the execution plan and confirm that
all supplied test cases are ready for execution.

Return:

TEST EXECUTION PLAN
Total Test Cases:
Test Case IDs:
Execution Order:
Validation:
"""
    )

    requirement_summary = "\n".join(
        [
            (
                f"{r['Test Case ID']} | "
                f"{r['Test Scenario']} | "
                f"{r['Test Input']}"
            )
            for r in requirements
        ]
    )

    manager_task = f"""
Review the following test requirements.

Requirements:

{requirement_summary}

Create the execution plan using exactly
the supplied test cases.
"""

    manager_response = await test_manager.run(
        task=manager_task
    )

    manager_output = (
        manager_response.messages[-1].content
    )

    print(manager_output)
    print()

    # ------------------------------------------------
    # STEP 3 - PLAYWRIGHT AGENT
    # ------------------------------------------------

    print("STEP 3: Playwright Agent")

    print(
        "Executing all repository-driven "
        "Playwright tests..."
    )

    print()

    results = run_all_playwright_tests()

    print()

    # ------------------------------------------------
    # STEP 4 - RESULT AGENT
    # ------------------------------------------------

    print("STEP 4: Result Agent")

    result_summary = await generate_result_summary(
        results
    )

    print()
    print(result_summary)
    print()

    # ------------------------------------------------
    # STEP 5 - REPORT AGENT
    # ------------------------------------------------

    print("STEP 5: Report Agent")

    report_file = write_execution_report(
        results
    )

    print(
        f"Report location: {report_file}"
    )

    # ------------------------------------------------
    # FINAL SUMMARY
    # ------------------------------------------------

    passed = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )

    failed = sum(
        1
        for result in results
        if result["status"] == "FAIL"
    )

    print()
    print("==================================================")
    print("FINAL AUTOMATION SUMMARY")
    print("==================================================")
    print()

    print(
        f"Total Test Cases : {len(results)}"
    )

    print(
        f"Passed           : {passed}"
    )

    print(
        f"Failed           : {failed}"
    )

    print(
        f"Excel Report     : {report_file}"
    )

    print()

    print(
        "AI Multi-Agent Test Automation completed."
    )

    print()

    await model_client.close()

    return {
        "requirements": requirements,
        "manager_output": manager_output,
        "results": results,
        "result_summary": result_summary,
        "report_file": str(report_file),
        "total": len(results),
        "passed": passed,
        "failed": failed,
    }


def run_test_automation_sync():

    return asyncio.run(
        run_test_automation()
    )


if __name__ == "__main__":

    run_test_automation_sync()