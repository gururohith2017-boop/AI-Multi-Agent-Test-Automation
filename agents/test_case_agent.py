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

    test_case_agent = AssistantAgent(
        name="TestCaseAgent",
        model_client=model_client,
        system_message="""
You are the Test Case Agent in a multi-agent web test automation system.

Your responsibility is to prepare an executable test plan from the
Test Manager's selected test case.

Use ONLY the following predefined test case information.

US-001:
Scenario: VPN / Internal IT
Test Input: My laptop VPN is not working. I am unable to connect to the company network.
Expected Result: Request routed to: Internal IT

US-002:
Scenario: Leave / HR
Test Input: I need to apply for leave. Can you tell me how to submit my leave request?
Expected Result: Request routed to: HR

US-003:
Scenario: Salary / Payroll
Test Input: My monthly salary has not been credited yet. Can you help me with my salary payment issue?
Expected Result: Request routed to: Payroll

US-004:
Scenario: Office Supplies / Admin
Test Input: I need help with an office administration request. Can you help me with the process for requesting office supplies?
Expected Result: Request routed to: Admin

US-005:
Scenario: Service Request / Help Desk
Test Input: I am having an issue with a service request. Can you help me check the status and provide support?
Expected Result: Request routed to: Help Desk

US-006:
Scenario: Compliance
Test Input: I have a question about company compliance requirements. Can you help me understand the compliance process?
Expected Result: Request routed to: Compliance

US-007:
Scenario: General Support / Auto Router
Test Input: I need help with a general corporate support request. Please guide me to the appropriate support team.
Expected Result: Request routed to the appropriate support agent.

US-008:
Scenario: Empty Input Validation
Test Input: Empty input
Expected Result: Send button remains disabled and no routing response is generated.

US-009:
Scenario: Ambiguous Query
Test Input: I need some help with something related to my work. Can you guide me to the right support team?
Expected Result: Request routed to an appropriate support agent.

US-010:
Scenario: Direct HR Agent Selection
Test Input: I have a question about the employee leave policy. Can you help me understand the process?
Expected Result: HR Agent is selected and processes the request.

When given a Test Case ID, return exactly:

Test Case ID:
Test Scenario:
Test Input:
Expected Result:
Execution Type:

Execution Type should be one of:
- Playwright UI Test
- Validation Test

Do not execute the test.
Do not invent test cases.
"""
    )

    task = """
The Test Manager selected:

Test Case ID: US-001
Test Scenario: VPN / Internal IT

Prepare the executable test plan for this test case.
"""

    result = await test_case_agent.run(task=task)

    print("\n========== TEST CASE AGENT RESULT ==========\n")
    print(result.messages[-1].content)
    print("\n============================================\n")

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())