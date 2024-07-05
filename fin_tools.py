from crewai_tools import tool
from langchain_community.tools import DuckDuckGoSearchResults 
import json
import yfinance as yf
import pandas as pd

# TOOLS

class SearchTool():

  @tool("search web tool")
  def search_web_tool(query):
    """
    Query the internet about a stock ticker last financial news and return up-to-date relevant results (use input: query)
    """
    search_tool = DuckDuckGoSearchResults(backend="news", num_results=5 , verbose=True)
    #search_tool = DuckDuckGoSearchResults(num_results=10 , verbose=True)
    return search_tool.run(query)

  # Tool Financial data tool
  @tool("financial data tool")
  def financial_data_tool(ticker):
      """
      Get all the financial data metrics for a given stock ticker name
      """
      # Fetch data for the company
      stock = yf.Ticker(ticker)
      # Initialize the document with the company's ticker
      document = f"Financial Data informations listed by the company with ticker {ticker} :\n ---- \n"
      # Get the info and reco
      document += "\n---\n ## Info and Financial metrics : \n" + str(stock.info)
      document += "\n---\n ## Recommendations : \n" + str(stock.recommendations)
      # Add news to the document
      news = stock.news
      out = "\n---\n ## News for the stock : \n"
      for i in news:
          out += f"# {i['title']} \n Publisher : {i['publisher']} \n Related ticker : {i['relatedTickers']} \n "
      document += out
      # balancesheet
      balance_sheet = pd.DataFrame(stock.balance_sheet)
      document += "\n---\n ## Balance Sheet : \n" + balance_sheet.to_string()
      # cash flow
      cash_flow = pd.DataFrame(stock.cashflow)
      document += "\n---\n ## Cash Flow : \n" + cash_flow.to_string()
      # income statement
      income_statement = pd.DataFrame(stock.income_stmt)
      document += "\n---\n ## Income Statement : \n" + income_statement.to_string()

      return document

    
  # Tool Financial statement tool
  @tool("financial tool")
  def fin_data_tool(ticker):
      """
      Get all the financial data metrics for a given stock ticker name
      """
      stock = yf.Ticker(ticker)
      return str(stock.info)

  # Tool Financial statement tool
  @tool("financial tool")
  def fin_statement_tool(ticker):
      """
      Get all the financial statements for a given stock ticker name
      """
      stock = yf.Ticker(ticker)
      balance_sheet = pd.DataFrame(stock.balance_sheet)
      cash_flow = pd.DataFrame(stock.cashflow)
      income_statement = pd.DataFrame(stock.income_stmt)
      doc = ""
      doc += "- Balance Sheet : \n" + balance_sheet.to_string()
      doc += "\n---\n- Cash Flow : \n" + cash_flow.to_string()
      doc += "\n---\n- Income Statement : \n" + income_statement.to_string()  
      return doc
