# server.py
from fastmcp import FastMCP, Context
import requests

# Base URL for the API
BASE_URL = "https://next.obudget.org"

# Constants
QUERY = "api/query"
SEARCH = "search"
BUDGET_QUERY = "SELECT parent, code, title, net_allocated, net_revised, net_executed FROM budget WHERE YEAR=2025 and depth < 3"
PARENT_BUDGET_QUERY = "SELECT parent, code, title, net_allocated, net_revised, net_executed FROM budget WHERE YEAR=2025 AND parent LIKE '{0}%%' "
BUDGET_HISTORY_QUERY = "SELECT history FROM budget WHERE YEAR=2025 AND code = '{0}'"
CONTRACTS_QUERY = " SELECT budget_code, min_year, coalesce(entity_name, supplier_name->>0) AS supplier,executed, purpose FROM contract_spending WHERE budget_code LIKE '{}%%' AND executed > 0 AND min_year > 2020"
SUPPORTS_QUERY = " SELECT budget_code, year_paid, coalesce(entity_name, recipient) AS supplier,amount_paid, support_title FROM supports_by_payment_year WHERE budget_code LIKE '{}%%' AND amount_paid > 0 AND year_paid > 2020"

# Create an MCP server with context support
mcp = FastMCP(
    "ILBudget",
    dependencies=["requests"],
    description="Israeli Budget Data API Server",
    allow_context=True,  # Enable context support
    context_prompt="""I can help you find information about the Israeli state budget.
                        You can ask me about:
                        - General search in the budget
                        - Information about a specific budget item
                        - Information about all items under a specific parent item
                        - History of a budget item
                        How can I assist you?"""
                        )
@mcp.tool()
async def get_supports(ctx: Context, code: str = "00"):
    """Get support payments and grants by budget code.
    
    Retrieves information about government support payments and grants given to various entities,
    filtered by a specific budget code. Only returns data from 2021 onwards where amount_paid > 0.

    Args:
        code (str): The budget code to search for.
        Must be a string with preserved leading zeros (e.g., use '0015' not '15').
        Defaults to "00" for all codes.
        
    Returns:
        dict: Contains support payment details including recipient, amount paid, year, and support title.
        Budget codes in results preserve leading zeros (e.g., '0015')."""

    await ctx.info("Searching for contracts for code {code}...")
    params = {
        "query": SUPPORTS_QUERY.format(str(code)),
        "page": 0
    }
    response = requests.get(f"{BASE_URL}/{QUERY}", params=params)
    response.raise_for_status()
    return response.json()

@mcp.tool()
async def get_contract(ctx: Context, code: str = "00"):
    """Get government contract spending data by budget code.
    
    Retrieves information about government contracts and spending, filtered by a specific budget code.
    Only returns contracts from 2021 onwards with executed amounts greater than 0.

    Args:
        code (str): The budget code to search for.
        Must be a string with preserved leading zeros (e.g., use '0015' not '15').
        Defaults to "00" for all codes.
        
    Returns:
        dict: Contains contract details including supplier name, executed amount, purpose, and year.
        Budget codes in results preserve leading zeros (e.g., '0015')."""

    await ctx.info("Searching for contracts for code {code}...")
    params = {
        "query": CONTRACTS_QUERY.format(str(code)),
        "page": 0
    }
    response = requests.get(f"{BASE_URL}/{QUERY}", params=params)
    response.raise_for_status()
    return response.json()

@mcp.tool()
async def get_budget(ctx: Context):
    """Get the high-level Israeli state budget structure.
    
    Retrieves the top-level budget items (depth < 3) for the current year,
    including allocated, revised, and executed amounts for each budget line.
    Budget codes are preserved as strings with leading zeros (e.g., '0015' stays as '0015').

    Returns:
        dict: Contains budget lines with their codes (as strings with preserved leading zeros), titles, and financial data
        including net_allocated, net_revised, and net_executed amounts.
        Example codes: '00', '0015', '001523'"""

    await ctx.info("Searching for available budget codes...")
    params = {
        "query": BUDGET_QUERY,
        "page": 0
    }
    response = requests.get(f"{BASE_URL}/{QUERY}", params=params)
    response.raise_for_status()
    return response.json()

@mcp.tool()
async def get_detailed_budget_for_specific_parent(ctx: Context, parent: str = "00"):
    """Get detailed budget information for a specific parent budget code.
    
    Retrieves all budget lines under a specific parent code, providing a detailed view
    of how the parent budget is broken down into sub-categories.

    Args:
        parent (str): The parent budget code to get details for.
        Must be a string with preserved leading zeros (e.g., use '0015' not '15').
        Defaults to "00" for top level.
        
    Returns:
        dict: Contains detailed budget information including codes (as strings with preserved leading zeros)
        , titles, allocations, revisions, and execution data for all items under the specified parent.
        Example parent codes: '00', '0015', '001523'"""

    await ctx.info(f"Searching budget for parent: {parent}...")
    params = {
        "query": PARENT_BUDGET_QUERY.format(str(parent)),
        "page": 0
    }
    response = requests.get(f"{BASE_URL}/{QUERY}", params=params)
    response.raise_for_status()
    return response.json()

@mcp.tool()
async def get_budget_history_for_code(ctx: Context, code: str = "00"):
    """Get the historical data for a specific budget code.
    
    Retrieves the full history of changes and allocations for a specific budget code,
    showing how the budget item has evolved over time.

    Args:
        code (str): The budget code to get history for.
        Must be a string with preserved leading zeros (e.g., use '0015' not '15').
        Defaults to "00".
        
    Returns:
        dict: Contains historical budget data including past allocations,
        revisions, and execution data for the specified budget code."""

    await ctx.info(f"Searching history for code: {code}...")
    params = {
        "query": BUDGET_HISTORY_QUERY.format(str(code)),
        "page": 0
    }
    response = requests.get(f"{BASE_URL}/{QUERY}", params=params)
    response.raise_for_status()
    return response.json()

@mcp.tool()
async def search(ctx: Context, searchTerm: str, searchType: str = "supports"):
    """Perform a text search across the Israeli budget database.
    
    Allows searching through different aspects of the budget system using free text.

    Args:
        searchTerm (str): The text to search for in the database.
        searchType (str): The type of data to search. Can be one of:
            - 'entities': Search government entities
            - 'national-budget-changes': Search budget modifications
            - 'supports': Search government grants and support payments
            - 'tenders': Search government tenders
            - 'contract-spending': Search government contracts
            
    Returns:
        dict: Contains search results matching the query within the specified category.
        Returns up to 20 results per page."""

    await ctx.info(f"Searching '{searchType}' for: {searchTerm}...")
    params = {
        "q": searchTerm,
        "size": 20,
        "offset": 0,    }
    response = requests.get(f"{BASE_URL}/{SEARCH}/{searchType}", params=params)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # This code only runs when the file is executed directly
    mcp.run()
