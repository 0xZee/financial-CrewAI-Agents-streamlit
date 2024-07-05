
import streamlit as st
import sys
from datetime import datetime, timedelta
from crewai import Crew, Process
from fin_agents import FinAgents, StreamToExpander
from fin_tasks import FinTasks
from template.fin_template import fin_template


st.set_page_config(page_icon="📝", page_title="ZeeFinReporter", layout="wide")

# class TravelCrew
class TravelCrew:

  def __init__(self, ticker):
      self.ticker = ticker
      self.output_placeholder = st.empty()

  def run(self):
      agents = FinAgents()
      tasks = FinTasks()

      fin_agent = agents.fin_agent()
      news_agent = agents.news_agent()
      reporter_agent = agents.reporter_agent()

      fin_task = tasks.fin_task(fin_agent, self.ticker)
      news_task = tasks.news_task(news_agent, self.ticker)
      reporter_task = tasks.reporter_task(
        [fin_task, news_task],
        reporter_agent,
        self.ticker,
      )

      crew = Crew(
        agents=[fin_agent, news_agent, reporter_agent],
        tasks=[fin_task, news_task, reporter_task],
        process=Process.sequential,
        full_output=True,
        share_crew=False,
        #llm=llm_groq,
        #manager_llm=llm,
        #max_iter=24,
        verbose=True
        )

      result = crew.kickoff()
      self.output_placeholder.markdown(result)

      return result


##
##
##
##

st.header("🏛️ Financial Reporter :orange[Ai]gent 📊", divider="orange")

# sidebar
with st.sidebar:
  st.caption("Financial Agent")
  st.markdown(
    """
    # 🏛️ Financial Reporter 📈
        1. Pick your dream destination
        2. give us your interests
        3. Set your travel dates
        4. Bon voyage !!
    """
  )
  st.divider()
  st.caption("Created by @0xZee")

st.session_state.plan_pressed = False
# User Inputs
today = datetime.now()

st.caption("🗺️ Let's plan your Financial Reporter")


# User Details container
ticker = st.text_input("📈 Your Stock Ticker :", placeholder="AAPL, TSLA...")

# out container
if ticker :
  st.caption("👌 Let's recap your Financial Report :")
  st.write(f":sparkles: 🎫 Financial Report for : {ticker} 📈.")
  if plan := st.button("💫 Sounds Good ! 🗺️ Generate The Report", use_container_width=True, key="plan"):
    st.write(ticker)
    with st.spinner(text="🤖 Agents working for the Financial Report 🔍 ..."):
      # RUN
      with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
        with st.container(height=300, border=False):
            sys.stdout = StreamToExpander(st)
            travel_crew = TravelCrew(ticker)
            result = travel_crew.run()
        status.update(label="✅ You Financial Report is Generated ! 📊",
                      state="complete", expanded=False)

      st.subheader(f"📊 Here is your {ticker} Financial Report 📰 ", anchor=False, divider="rainbow")
      st.markdown(result["final_output"])
      st.divider()
      # Display each key-value pair in 'usage_metrics'
      st.json(result['usage_metrics'])
      st.divider()
      # expander for each 'exported_output'
      for i, task in enumerate(result['tasks_outputs']):
          with st.expander(f"Agent Report {i+1} :", expanded=False):
              st.markdown(task)
      st.divider()










