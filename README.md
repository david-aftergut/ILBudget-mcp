# ILBudget-mcp

MCP Server for accessing Israeli budget data through the OpenBudget API.

## Description

This project provides a FastMCP server that interfaces with Israel's OpenBudget data.</br>
Allowing easy access to budget data, contracts, and supports information.</br>
It serves as a bridge between the OpenBudget API and MCP clients.

This project is possible only thanks to amazing work of [OpenBudget/BudgetKey](https://github.com/OpenBudget/BudgetKey) team.</br>
See their [UsingTheAPI](https://github.com/OpenBudget/BudgetKey/blob/master/documentation/UsingTheAPI.md) for more details about the API used in this MCP server.</br>
If you wish to craft your own queries or tool you can use their [Redash](http://data.obudget.org/) to test them (You can see my queries in [ILBudgetServer.py](ILBudgetServer.py)).

## Features

- Full access to Israel's governmental budget data
- Real-time integration with the OpenBudget API
- Comprehensive search capabilities across multiple data categories
- Historical budget tracking and analysis
- Contract and support payment information retrieval
- Easy-to-use MCP interface for client applications

## Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager

## Installation

```bash
git clone <repository-url>
cd ILBudget-mcp
uv venv
.venv\Scripts\activate
uv pip install -r pyproject.toml
uv lock
```

## Usage

Install and run the server using one of these methods:

1. For use with [Claude AI Assistant](https://claude.ai) or [Visual Studio Code (using Copilot)](https://code.visualstudio.com/download):
```bash
fastmcp install ILBudgetServer.py
```

2. For testing with MCP Inspector (Learn how at [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)):
```bash
fastmcp dev ILBudgetServer.py
```

### Available Tools

- `get_budget()` - Retrieves the entire budget structure
- `get_detailed_budget_for_specific_parent(parent)` - Gets detailed budget items under a specific parent
- `get_budget_history_for_code(code)` - Retrieves historical data for a specific budget code
- `get_contract(code)` - Gets contract information for a specific budget code
- `get_supports(code)` - Retrieves support payment information for a specific budget code
- `search(searchTerm, searchType)` - Performs a general search across different categories

## Dependencies

- fastmcp >= 2.1.1
- requests >= 2.32.3

## Contributing

We welcome contributions to help improve the DataGov Israel MCP server.</br>
Whether you want to add new tools, enhance existing functionality, or improve documentation, your input is valuable.

For examples of other MCP servers and implementation patterns, see the [Model Context Protocol servers repository](https://github.com/modelcontextprotocol/servers).

## License

This project is dual-licensed under:
- MIT License
- Creative Commons Attribution-ShareAlike 4.0 International License

See the [LICENSE](LICENSE) file for details.