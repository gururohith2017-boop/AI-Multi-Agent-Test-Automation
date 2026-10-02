import os
import asyncio

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.requirement_reader import load_requirements


load_dotenv()


async def main():

    print()
    print("==============================================")
    print("AI REQUIREMENT MANAGER")
    print("==============================================")
    print()

    # =====================================================
    # 1. LOAD REQUIREMENTS FROM EXCEL
    # =====================================================

    requirements = load_requirements()

    print(
        f"Requirements loaded from Excel: {len(requirements)}"
    )

    # =====================================================
    # 2. PREPARE REQUIREMENTS FOR AUTOGEN
    # =====================================================

    requirement_text = ""

    for requirement in requirements:

        requirement_text += f"""
Test Case ID: {requirement['Test Case ID']}
User Story: {requirement['User Story']}
Test Scenario: {requirement['Test Scenario']}
Test Input: {requirement['Test Input']}
Expected Result: {requirement['Expected Result']}

----------------------------------------
"""

    # =====================================================
    # 3. CREATE OPENAI MODEL CLIENT
    # =====================================================

    model = os.getenv(
        "OPENAI_MODEL",
        "gpt-4o-mini"
    )

    model_client = OpenAIChatCompletionClient(
        model=model
    )

    # =====================================================
    # 4. CREATE TEST MANAGER AGENT
    # =====================================================

    test_manager = AssistantAgent(
        name="TestManager",
        model_client=model_client,
        system_message="""
You are the Test Manager Agent in an AI-powered
web test automation framework.

You receive test requirements from the Requirement Repository.

Your responsibility is to analyze the supplied requirements
and identify the test cases that should be executed.

IMPORTANT RULES:

1. Use ONLY the Test Case IDs provided in the requirements.
2. Do NOT invent Test Case IDs.
3. Do NOT modify the Test Input.
4. Do NOT modify the Expected Result.
5. Do NOT execute Playwright.
6. Return all available executable test cases.

Return the result in this format:

EXECUTION PLAN

Test Case ID: US-001
Scenario: ...

Test Case ID: US-002
Scenario: ...

etc.
"""
    )

    # =====================================================
    # 5. SEND REQUIREMENTS TO TEST MANAGER
    # =====================================================

    task = f"""
The following requirements were loaded from the
customer support requirement repository.

Create the execution plan for these requirements.

{requirement_text}
"""

    print()
    print("Sending requirements to Test Manager Agent...")
    print()

    result = await test_manager.run(
        task=task
    )

    manager_output = result.messages[-1].content

    # =====================================================
    # 6. DISPLAY RESULT
    # =====================================================

    print()
    print("==============================================")
    print("TEST MANAGER EXECUTION PLAN")
    print("==============================================")
    print()

    print(manager_output)

    print()
    print("==============================================")
    print("REQUIREMENT MANAGEMENT COMPLETED")
    print("==============================================")
    print()

    # =====================================================
    # 7. CLOSE MODEL CLIENT
    # =====================================================

    await model_client.close()


if __name__ == "__main__":

    asyncio.run(main())