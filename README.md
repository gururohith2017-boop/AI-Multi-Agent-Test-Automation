Architecture
             Excel Requirements
                     │
                     ▼
           Requirement Reader
                     │
                     ▼
           Test Manager Agent
              (AutoGen Agent)
                     │
                     ▼
           Test Case Repository
             (Deterministic)
                     │
                     ▼
             Playwright Agent
                     │
                     ▼
        Live Customer Support App
                     │
                     ▼
               Result Agent
              (AutoGen Agent)
                     │
                     ▼
               Report Agent
                     │
                     ▼
            Excel Test Report
                     │
                     ▼
            Streamlit Dashboard


--------------------------------------------------------------------
I have implemented an AI-powered multi-agent test automation framework using AutoGen, Playwright, Python, Excel and Streamlit.

The objective is to automate testing of a corporate customer-support application using requirements maintained in an Excel file.

The Excel file acts as the single source of truth for the user stories, test scenarios, test inputs and expected results.

First, the Requirement Reader loads the requirements from Excel. Then the Test Manager Agent, which is an AutoGen agent, validates and organizes the test execution plan.

The test cases are maintained in a deterministic Test Case Repository. This is important because I don't want the LLM to randomly generate test data or expected results during execution.

Next, the Playwright Agent picks each test case and executes the corresponding browser automation against the live customer-support application. It validates the routing behavior, captures screenshots and returns structured PASS or FAIL results.

After execution, the Result Agent analyzes the execution results and provides an overall summary.

Finally, the Report Agent generates an Excel execution report containing the test case, expected result, actual result, status, execution duration, timestamp, screenshot and error details.

I also created a Streamlit dashboard where the complete process can be triggered using one button. So there is no need for the user to manually enter each query.

In my latest execution, all 10 repository-driven test cases passed successfully with 0 failures.

The key design principle is that I use AI where it adds value, such as orchestration and result analysis, while keeping test data, browser execution and PASS/FAIL validation deterministic


--------------------------------------------------------------------------------------------


1. Why did you use AutoGen?

Answer:

“I used AutoGen for multi-agent orchestration. Instead of putting the complete responsibility into one LLM, I separated responsibilities such as test management and result analysis. This makes the architecture more modular and easier to extend.”

2. How many agents do you have?

Say this carefully:

“I have two actual AutoGen agents currently — the Test Manager Agent and Result Agent. The Playwright Agent is an execution component rather than an LLM agent. The Test Case Repository and Requirement Reader are deterministic components.”

This is a very good architectural answer because you're not calling every Python module an AI agent.

3. Why isn't the LLM generating the test cases?

“For production-quality automation, I wanted repeatability and control. The requirements and expected results come from Excel, so the LLM cannot hallucinate test inputs or expected behavior. AI is used for orchestration and analysis, while the actual test execution remains deterministic.”

4. Why Playwright?

“Playwright provides reliable browser automation and supports modern web applications. It also gives me browser-level validation, element interaction, assertions, screenshots and cross-browser capability.”

5. What happens when a test fails?

“Playwright returns a non-zero execution status. My Playwright Agent captures the failure details and screenshot. The Result Agent then includes the failed test in the overall analysis, and the Report Agent records the failure and error details in Excel.”

6. How do you calculate PASS/FAIL?

“The primary PASS/FAIL decision comes from the deterministic Playwright execution result. The Result Agent analyzes and summarizes those results rather than inventing a status.”

7. How do you scale this framework?

“I can add a new requirement row to the Excel repository and create the corresponding Playwright test mapped to that Test Case ID. The central workflow can then discover and execute it without changing the overall architecture.”

8. Why Excel?

“Excel is simple for business users and testers to maintain. It also provides an auditable source of requirements, test inputs and expected results.”

9. What is the role of Streamlit?

“Streamlit provides the execution dashboard. It displays the requirements, execution progress, PASS/FAIL summary, Result Agent analysis, screenshots and provides access to the generated Excel report.”

10. What is the biggest advantage of your architecture?

“The main advantage is the separation between AI reasoning and deterministic test execution. AI handles orchestration and analysis, while the repository and Playwright provide repeatable execution.”


--------------------------------------------------------------------------------

"Is this really Agentic AI?"

A strong answer:

“Yes, in a controlled form. The architecture uses autonomous task-oriented components where the Test Manager Agent handles test execution planning and the Result Agent analyzes execution outcomes. However, I intentionally keep browser execution deterministic rather than allowing an LLM to freely interact with the application. This gives us better reliability and governance.”

That's a much stronger answer than simply saying "everything is an AI agent."
-----------------------------------------------------------------------------------
💡 One sentence to remember


“AI manages the intelligence layer; Playwright manages the execution layer; Excel manages the test truth; and Streamlit provides the visibility layer.”

That one sentence can help you explain the entire project clearly.

-----------------------------------------------------------