import os
import asyncio
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


load_dotenv()


async def main():
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    model_client = OpenAIChatCompletionClient(
        model=model
    )

    test_manager = AssistantAgent(
        name="TestManager",
        model_client=model_client,
        system_message="""
You are the Test Manager Agent for a web test automation system.

Your responsibility is to analyze the user's testing request and identify
the appropriate existing test case from the corporate customer support
application.

Available test cases:

US-001 - VPN / Internal IT
US-002 - Leave / HR
US-003 - Salary / Payroll
US-004 - Office Supplies / Admin
US-005 - Service Request / Help Desk
US-006 - Compliance
US-007 - General Support / Auto Router
US-008 - Empty Input Validation
US-009 - Ambiguous Query
US-010 - Direct HR Agent Selection

Return the following information:

Test Case ID:
Test Scenario:
Test Input:
Expected Result:

Do not execute the test.
Only identify the appropriate test case.
"""
    )

    task = """
I want to test the customer support application with this request:

"My laptop VPN is not working. I am unable to connect to the company network."

Identify the appropriate test case.
"""

    result = await test_manager.run(task=task)

    print("\n========== TEST MANAGER RESULT ==========\n")
    print(result.messages[-1].content)
    print("\n=========================================\n")

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())