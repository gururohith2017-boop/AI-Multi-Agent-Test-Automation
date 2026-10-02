import asyncio
import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.playwright_agent import run_all_playwright_tests


load_dotenv()


async def generate_result_summary(results):

    model = os.getenv(
        "OPENAI_MODEL",
        "gpt-4o-mini"
    )

    model_client = OpenAIChatCompletionClient(
        model=model
    )

    result_agent = AssistantAgent(
        name="ResultAgent",
        model_client=model_client,
        system_message="""
You are the Result Agent in a multi-agent
test automation system.

Your responsibility is to analyze the execution
results produced by the Playwright Agent.

Use ONLY the execution results provided.

Do not invent test results.

IMPORTANT:

If Failed = 0:
    Overall Result must be PASS.

If Failed > 0:
    Overall Result must be FAIL.

The Overall Result must always match the
actual Passed and Failed counts.

Return exactly this structure:

TEST EXECUTION SUMMARY
----------------------

Total Test Cases:
Passed:
Failed:

Test Case Results:
US-001: PASS/FAIL
US-002: PASS/FAIL
...
US-010: PASS/FAIL

Overall Result:
PASS or FAIL

Summary:
Provide a short factual summary of the execution.
"""
    )

    result_lines = []

    for result in results:

        result_lines.append(
            f"{result['test_case_id']}: "
            f"{result['status']}"
        )

    result_text = "\n".join(
        result_lines
    )

    total = len(results)

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

    if failed == 0:
        overall_result = "PASS"
    else:
        overall_result = "FAIL"

    task = f"""
Analyze the following Playwright execution results.

Total Test Cases: {total}
Passed: {passed}
Failed: {failed}

The calculated Overall Result is:

{overall_result}

Execution Results:

{result_text}

Generate the required test execution summary.

The Overall Result MUST be:

{overall_result}
"""

    response = await result_agent.run(
        task=task
    )

    await model_client.close()

    return response.messages[-1].content


async def main():

    print()
    print(
        "=============================================="
    )
    print(
        "RESULT AGENT"
    )
    print(
        "=============================================="
    )
    print()

    print(
        "Running Playwright Agent "
        "to obtain execution results..."
    )

    print()

    results = run_all_playwright_tests()

    print()
    print(
        "Playwright execution completed."
    )

    print()

    summary = await generate_result_summary(
        results
    )

    print()
    print(
        "=============================================="
    )
    print(
        "RESULT AGENT SUMMARY"
    )
    print(
        "=============================================="
    )
    print()

    print(summary)

    print()

    print(
        "=============================================="
    )
    print(
        "RESULT AGENT COMPLETED"
    )
    print(
        "=============================================="
    )


if __name__ == "__main__":

    asyncio.run(main())