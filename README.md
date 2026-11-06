# Ecommerce AI Agent System

A Python-based multi-agent ecommerce research system designed to discover, evaluate, and monitor potential products for online marketplaces.

## Project Overview

The goal is to build a system where specialized AI agents work together to research products, analyze profitability, identify market trends, and recommend business opportunities.

The project is currently under active development.

## Current Features

- Product profit and profit margin calculations
- Weighted opportunity scoring
- SQLite database for product storage
- Product search and deletion
- Product watchlist management
- Automated product ranking
- AI-powered product analysis using the OpenAI API
- JSON reports for sharing product information
- Research queue generation

## Technologies Used

- Python
- SQLite
- OpenAI API
- JSON
- Git and GitHub

## Project Architecture

- `main.py` - Main product evaluation program
- `product_evaluator.py` - Profit and opportunity calculations
- `database.py` - Database operations
- `manager_agent.py` - Product ranking and AI analysis
- `ai_analyzer.py` - OpenAI API integration
- `research_agent.py` - Research queue preparation

## Development Roadmap

- [x] Build product evaluation system
- [x] Create SQLite database
- [x] Implement product watchlists
- [x] Build automated product ranking
- [x] Connect OpenAI API
- [x] Generate AI-powered recommendations
- [ ] Integrate eBay marketplace research
- [ ] Implement automated trend detection
- [ ] Enable communication between agents
- [ ] Build a graphical dashboard
- [ ] Deploy the system to a dedicated home server

## Current Limitations

Product demand and competition are currently entered manually.

The Research Agent prepares research tasks but does not yet collect live marketplace data.

AI recommendations require additional verification before purchasing or listing products.

## Project Status

Active development - Python foundations and initial AI integration completed.
