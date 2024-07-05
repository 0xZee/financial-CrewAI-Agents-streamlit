from datetime import datetime
from crewai import Task
from agents import location_expert, guide_expert, planner_expert
#DuckDuckGoSearchRunTool DuckDuckGoSearchResults DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from template import fin_template, news_template




# TASKS
class FinTasks():

    # Task: financial data
    def fin_task(self, agent, ticker):
        return Task(
            description=f"""
            Use the financial data tool to gather the financial metrics for company {ticker}, and 
            Format them in tables using {fin_template} template.
            """,
            expected_output=f"""Here is an example of a financial report {ticker} template to use :
            <Template>
            {fin_template}
            </Template>
            """,
            agent=agent,
            #context=context,
            output_file='financial_report.md',
        )

    # Task: news
    def news_task(self, agent, ticker):
        return Task( 
            description=f"""
            Use the search news tool to get the last 10 news about company {ticker}.
            Categorize the news into Bullish, Bearish, Neutral.
            Perform an in-depth analysis of these news to establish outlook, insights, and future trends
            """,
            expected_output=f"""Here is an example of a financial report {ticker} template to use :
            <Template>
            {news_template}
            </Template>
            """,
            agent=agent,
            output_file='news_report.md',
        )

    # Task: reporter
    def reporter_task(self, context, agent, ticker):
        return Task(
            description=f"""
            Use both reports provided by the Financial Analyst and the News Analyst to create the final {ticker} financial report :
            The current date is {datetime.now()}
            Provide a summary at the beginning of the report with presentation of the company and the industry market and key takeaways for quick reference.
            Present first the the Financial Analyst report and the News Analyst report in markdown format, include for each paragraph a table with related data
            Look for the risks and tailwinds and identify futur trends.
            Add a section on market sentiment analysis using news trends to provide a more comprehensive view.
            Conduct a Highly detailed analysis of ticker's financial data.
            In a Data Annexe Section : Provide a brief overview of the stock’s main finance data in table format to give the user more precices inputs.
            Conculsion at the end of the report highlighting the main news and trends.
            """,
            expected_output="Full Financial report for {ticker} in rich markdown format, Your report should be lowlevel detailed and informative, catering to a professional audience. Make it sound professional, provide full analysis, introduction and conclusion",
            agent=agent,
            context=context,
            output_file='global_report.md',
        )

    # tip section
    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $1000 and grant you any wish you want!"
