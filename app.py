import streamlit as st
from pathlib import Path
import pandas as pd

from agents.requirement_reader import load_requirements
from agents.test_automation_workflow import (
    run_test_automation_sync,
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

REQUIREMENT_FILE = (
    PROJECT_ROOT
    / "user_stories"
    / "customer_support_user_stories.xlsx"
)

REPORT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "test_execution_report.xlsx"
)


# ============================================================
# STREAMLIT CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Multi-Agent Test Automation",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 AI Multi-Agent Test Automation"
)

st.markdown(
    """
### Requirement-to-Execution Automation Platform

**AutoGen + Playwright + Excel + Streamlit**

This application demonstrates an AI-powered multi-agent
test automation workflow where test requirements are read
from Excel, validated by the Test Manager Agent, executed
using Playwright, analyzed by the Result Agent, and published
into an Excel execution report.
"""
)

st.divider()


# ============================================================
# LOAD REQUIREMENTS
# ============================================================

st.subheader(
    "📄 Requirement Source"
)

col1, col2 = st.columns([4, 1])

with col1:

    st.info(
        "📁 customer_support_user_stories.xlsx"
    )

    if REQUIREMENT_FILE.exists():

        try:

            requirements = load_requirements()

            st.success(
                "Requirement file loaded successfully."
            )

        except Exception as error:

            requirements = []

            st.error(
                f"Unable to load requirement file: {error}"
            )

    else:

        requirements = []

        st.error(
            "Requirement file not found."
        )


with col2:

    st.metric(
        "Test Cases",
        len(requirements)
    )


# ============================================================
# REQUIREMENT PREVIEW
# ============================================================

st.subheader(
    "🧪 Test Case Repository"
)

if requirements:

    preview_data = []

    for requirement in requirements:

        preview_data.append(
            {
                "Test Case ID":
                    requirement["Test Case ID"],

                "Scenario":
                    requirement["Test Scenario"],

                "Test Input":
                    requirement["Test Input"],

                "Expected Result":
                    requirement["Expected Result"],
            }
        )

    dataframe = pd.DataFrame(
        preview_data
    )

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.warning(
        "No test cases available."
    )


st.divider()


# ============================================================
# AUTOMATION EXECUTION
# ============================================================

st.subheader(
    "▶ Automation Execution"
)

st.write(
    "The complete automation will automatically read "
    "the supplied requirements from Excel and execute "
    "all repository-driven Playwright test cases."
)

run_automation = st.button(
    "▶ RUN FULL AUTOMATION",
    type="primary",
    use_container_width=True,
)


# ============================================================
# RUN AUTOMATION
# ============================================================

if run_automation:

    if not requirements:

        st.error(
            "No test cases are available for execution."
        )

    else:

        progress = st.progress(0)

        status_placeholder = st.empty()

        try:

            # ------------------------------------------------
            # TEST MANAGER
            # ------------------------------------------------

            status_placeholder.info(
                "🤖 Test Manager Agent — "
                "validating requirements..."
            )

            progress.progress(10)

            # ------------------------------------------------
            # AUTOMATION WORKFLOW
            # ------------------------------------------------

            status_placeholder.info(
                "🎭 Playwright Agent — "
                "executing automated test cases..."
            )

            progress.progress(30)

            result = run_test_automation_sync()

            progress.progress(90)

            # ------------------------------------------------
            # COMPLETION
            # ------------------------------------------------

            progress.progress(100)

            status_placeholder.success(
                "✅ AI Multi-Agent Test Automation completed."
            )


            # =================================================
            # EXECUTION SUMMARY
            # =================================================

            st.divider()

            st.subheader(
                "📊 Test Execution Summary"
            )

            total = result["total"]

            passed = result["passed"]

            failed = result["failed"]


            summary_col1, summary_col2, summary_col3 = (
                st.columns(3)
            )


            with summary_col1:

                st.metric(
                    "Total Test Cases",
                    total
                )


            with summary_col2:

                st.metric(
                    "Passed",
                    passed
                )


            with summary_col3:

                st.metric(
                    "Failed",
                    failed
                )


            # =================================================
            # OVERALL RESULT
            # =================================================

            st.divider()

            if failed == 0:

                st.success(
                    "🎉 OVERALL RESULT: PASS\n\n"
                    "All test cases executed successfully."
                )

            else:

                st.error(
                    f"OVERALL RESULT: FAIL\n\n"
                    f"{failed} test case(s) failed."
                )


            # =================================================
            # AGENT EXECUTION STATUS
            # =================================================

            st.divider()

            st.subheader(
                "🤖 Multi-Agent Execution Status"
            )

            agent_col1, agent_col2 = st.columns(2)


            with agent_col1:

                st.success(
                    "✅ Test Manager Agent — Completed"
                )

                st.success(
                    "✅ Test Case Repository — Loaded"
                )

                st.success(
                    "✅ Playwright Agent — Completed"
                )


            with agent_col2:

                st.success(
                    "✅ Result Agent — Completed"
                )

                st.success(
                    "✅ Report Agent — Completed"
                )

                st.success(
                    "✅ Excel Report — Generated"
                )


            # =================================================
            # DETAILED TEST RESULTS
            # =================================================

            st.divider()

            st.subheader(
                "🧪 Detailed Test Results"
            )

            result_data = []

            for test_result in result["results"]:

                result_data.append(
                    {
                        "Test Case ID":
                            test_result["test_case_id"],

                        "Scenario":
                            test_result["test_scenario"],

                        "Status":
                            test_result["status"],

                        "Duration":
                            test_result[
                                "execution_duration"
                            ],

                        "Actual Result":
                            test_result[
                                "actual_result"
                            ],

                        "Screenshot":
                            test_result[
                                "screenshot"
                            ],
                    }
                )


            results_dataframe = pd.DataFrame(
                result_data
            )


            st.dataframe(
                results_dataframe,
                use_container_width=True,
                hide_index=True,
            )


            # =================================================
            # RESULT AGENT ANALYSIS
            # =================================================

            st.divider()

            st.subheader(
                "🔍 Result Agent Analysis"
            )

            st.text(
                result["result_summary"]
            )


            # =================================================
            # EXCEL REPORT
            # =================================================

            st.divider()

            st.subheader(
                "📊 Excel Execution Report"
            )

            st.write(
                "Fresh execution report generated at:"
            )

            st.code(
                result["report_file"]
            )


            if REPORT_FILE.exists():

                with open(
                    REPORT_FILE,
                    "rb"
                ) as report:

                    st.download_button(
                        label="⬇ Download Excel Report",
                        data=report,
                        file_name=(
                            "test_execution_report.xlsx"
                        ),
                        mime=(
                            "application/"
                            "vnd.openxmlformats-officedocument."
                            "spreadsheetml.sheet"
                        ),
                        use_container_width=True,
                    )


            # =================================================
            # SCREENSHOT REPORT
            # =================================================

            st.divider()

            st.subheader(
                "📸 Execution Screenshots"
            )

            screenshot_data = []

            for test_result in result["results"]:

                screenshot_path = (
                    test_result["screenshot"]
                )

                screenshot_file = (
                    PROJECT_ROOT
                    / screenshot_path
                )

                screenshot_data.append(
                    {
                        "Test Case ID":
                            test_result[
                                "test_case_id"
                            ],

                        "Status":
                            test_result[
                                "status"
                            ],

                        "Screenshot":
                            screenshot_path,

                        "Available":
                            (
                                "Yes"
                                if screenshot_file.exists()
                                else "No"
                            ),
                    }
                )


            screenshot_dataframe = pd.DataFrame(
                screenshot_data
            )


            st.dataframe(
                screenshot_dataframe,
                use_container_width=True,
                hide_index=True,
            )


            # =================================================
            # DEMO ARCHITECTURE
            # =================================================

            st.divider()

            st.subheader(
                "🏗️ Automation Architecture"
            )

            st.code(
                """
User Story / Requirement Excel
            │
            ▼
   Requirement Reader
            │
            ▼
    Test Manager Agent
            │
            ▼
   Test Case Repository
            │
            ▼
      Playwright Agent
            │
            ▼
 Customer Support Application
            │
            ▼
       Result Agent
            │
            ▼
       Report Agent
            │
            ▼
     Excel Test Report
                """,
                language="text"
            )


        except Exception as error:

            progress.progress(100)

            status_placeholder.error(
                "❌ Automation execution failed."
            )

            st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Multi-Agent Test Automation | "
    "AutoGen + Playwright + Excel + Streamlit"
)
