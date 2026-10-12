import streamlit as st
import pandas as pd
from src.planner import plan_week, answer_question, forward_chain

st.set_page_config(page_title="Weather Activity Planner", page_icon="🌦️", layout="wide")

st.title("🌦️ Weather-Based Activity Planner")
st.caption("Assignment 2 • Manual weather input • CSP planning • Explainable rules")
st.info("Enter sample forecast details for each day. This demo does not fetch live weather data.")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
activities = ["Cycling", "Sports practice", "Picnic", "Laundry drying",
              "Outdoor study", "Indoor study", "Indoor games", "Rest"]

with st.sidebar:
    st.header("Planning preferences")
    preferred_activity = st.selectbox("Preferred activity", activities)
    st.caption("The planner will try to include this activity when conditions allow.")
    st.markdown("---")
    st.markdown("**Safety note**")
    st.caption("This is an educational decision-support demo, not medical advice. Check official weather and air-quality guidance.")

st.subheader("1. Enter the weekly forecast")
st.write("Change the sample values below to match your assignment test case.")

default_rows = []
for i, day in enumerate(days):
    default_rows.append({
        "Day": day,
        "Temperature °C": [28, 30, 29, 32, 27, 31, 28][i],
        "Rain chance %": [10, 70, 20, 15, 40, 80, 10][i],
        "AQI": [45, 55, 60, 70, 50, 65, 40][i],
        "Wind km/h": [10, 12, 14, 18, 11, 20, 9][i],
        "Available": True
    })

forecast = st.data_editor(
    pd.DataFrame(default_rows),
    hide_index=True,
    use_container_width=True,
    disabled=["Day"],
    column_config={
        "Temperature °C": st.column_config.NumberColumn(min_value=-10, max_value=55, step=1),
        "Rain chance %": st.column_config.NumberColumn(min_value=0, max_value=100, step=5),
        "AQI": st.column_config.NumberColumn(min_value=0, max_value=500, step=5),
        "Wind km/h": st.column_config.NumberColumn(min_value=0, max_value=150, step=1),
        "Available": st.column_config.CheckboxColumn()
    }
)

if st.button("✨ Generate weekly plan", type="primary", use_container_width=True):
    records = forecast.to_dict("records")
    result = plan_week(records, preferred_activity)
    st.session_state["plan_result"] = result
    st.session_state["forecast_records"] = records

if "plan_result" in st.session_state:
    result = st.session_state["plan_result"]
    st.subheader("2. Your recommended weekly plan")
    st.success(f"Plan created. Search nodes: {result['nodes']} | Backtracks: {result['backtracks']} | AC-3: {result['ac3_removed']} domain values removed")
    st.dataframe(pd.DataFrame(result["plan"]), use_container_width=True, hide_index=True)

    st.subheader("3. Why were these activities selected?")
    for item in result["plan"]:
        with st.expander(f"{item['Day']} — {item['Activity']} (utility {item['Expected utility']}/100)"):
            st.write(item["Explanation"])
            st.write(f"Suitability estimate: {item['Suitability']}%")
            if item["Warnings"]:
                st.warning(" • ".join(item["Warnings"]))
            else:
                st.info("No warning was triggered by the entered values. This does not guarantee safety.")

    st.subheader("4. Ask the rule engine")
    selected_day = st.selectbox("Choose a day", days, key="question_day")
    question_activity = st.selectbox("Activity to check", activities, index=0, key="question_activity")
    if st.button("Can I do this activity?"):
        row = next(r for r in st.session_state["forecast_records"] if r["Day"] == selected_day)
        answer = answer_question(row, question_activity)
        if answer["status"] == "Suitable":
            st.success(answer["answer"])
        elif answer["status"] == "Not recommended":
            st.warning(answer["answer"])
        else:
            st.info(answer["answer"])
        st.write("**Backward-chaining trace:**")
        for step in answer["trace"]:
            st.write(f"- {step}")

    with st.expander("View CSP and inference details"):
        st.markdown("**CSP variables:** one variable for each day.")
        st.markdown("**Domains:** the activity list, filtered by availability and safety rules.")
        st.markdown("**Backtracking:** tries activities and returns to an earlier day if a later day has no valid option.")
        st.markdown("**AC-3:** revises adjacent day domains using the simple rule that the same activity should not be repeated on consecutive days, where alternatives exist.")
        st.markdown("**Forward chaining:** entered facts → matching rules → recommendation.")
        for row in st.session_state["forecast_records"]:
            with st.expander(f"Forward-chaining trace: {row['Day']}"):
                trace = forward_chain(row)
                st.write("**Known facts**")
                for fact in trace["facts"]:
                    st.write(f"- {fact}")
                st.write("**Conclusions**")
                for conclusion in trace["conclusions"]:
                    st.write(f"- {conclusion}")
        st.markdown("**Uncertainty:** a transparent suitability score is used as a simple heuristic, not a medically validated probability.")
        st.markdown("**Expected utility:** estimated suitability plus a preference bonus, with safety restrictions applied first.")

st.divider()
st.caption("Responsible AI: recommendations depend on manual inputs and simplified rules. Missing or inaccurate data can change the result. Not medical advice.")
