import streamlit as st
from crewai import Agent
from langchain_groq import ChatGroq
from fin_tools import SearchTool
import re


# AGENTS
class FinAgents():

    def llm(self):
        llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0, api_key=st.secrets['GROQ_API']) # model="llama3-70b-8192"
        return llm

    # Financial expert
    def fin_agent(self):
        return Agent(
            role="Financial Analyst",
            goal="Uncover main financial situation and insights about company {ticker}",
            backstory="""You work at an asset management firm analyst.
            Higly skilled in analyzing stock {ticker} data based of the financial data.""",
            verbose=True,
            memory=True,
            max_iter=5,
            allow_delegation=False,
            tools=[SearchTool.fin_data_tool],
            llm = self.llm(),
        )
        
    # news expert
    def news_agent(self):
        return Agent(
            role="News Analyst",
            goal="Uncover news and market sentiments about the company {ticker}",
            backstory="""You work at an news office for asset management firm.
          Your goal is to get and categorize news of the stock {ticker} and identify trends.""",
            verbose=True,
            memory=True,
            max_iter=5,
            allow_delegation=False,
            tools=[SearchTool.search_web_tool],
            llm = self.llm(),
        )

    # reporter expert
    def reporter_agent(self):
        return Agent(
            role="Financial Reporter",
            goal="Craft compelling and detailed content on financial report for the stock {ticker}",
            backstory="""You are a renowned Content Strategist for {ticker}, known for your insightful and engaging articles.
          You transform complex concepts into compelling narratives.""",
            verbose=True,
            memory=True,
            max_iter=5,
            allow_delegation=False,
            llm = self.llm()
        )




class StreamToExpander:
    # Print agent process to Streamlit app container 
    # This portion of the code is adapted from @AbubakrChan; thank you!  

    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary

            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "City Selection Expert" in cleaned_data:
            # Apply different color 
            cleaned_data = cleaned_data.replace("City Selection Expert", f":{self.colors[self.color_index]}[City Selection Expert]")
        if "Local Expert at this city" in cleaned_data:
            cleaned_data = cleaned_data.replace("Local Expert at this city", f":{self.colors[self.color_index]}[Local Expert at this city]")
        if "Amazing Travel Concierge" in cleaned_data:
            cleaned_data = cleaned_data.replace("Amazing Travel Concierge", f":{self.colors[self.color_index]}[Amazing Travel Concierge]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []
