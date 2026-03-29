# FlavourFind 🍽️

An AI-powered restaurant discovery agent built for Gen AI Academy Cohort 1 — Track 2.

FlavourFind uses Google ADK and MCP Toolbox for Databases to let users discover restaurants through natural language queries, powered by real Yelp data stored in BigQuery.

---

## Architecture
```
User → ADK Agent (Cloud Run) → MCP Toolbox (Cloud Run) → BigQuery
                ↓
          Vertex AI (Gemini 2.5 Flash)
```

- **ADK Agent** — Gemini 2.5 Flash powered conversational agent
- **MCP Toolbox** — Self-hosted MCP server that exposes BigQuery as tools
- **BigQuery** — `flavourfind.restaurants` table with 34,987 Yelp restaurant records

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `search_by_cuisine_and_location` | Find restaurants by cuisine type and city |
| `top_rated_restaurants` | Get highest rated restaurants in a city |
| `search_with_wifi` | Find restaurants offering free WiFi in a city |

---

## Live Demo

**Agent API (Cloud Run):**
`https://adk-agent-135138907357.us-central1.run.app`

**MCP Toolbox (Cloud Run):**
`https://mcp-toolbox-135138907357.us-central1.run.app`

### Sample API call
```bash
# Step 1 — Create a session
SESSION_ID=$(curl -s -X POST https://adk-agent-135138907357.us-central1.run.app/apps/adk_agent/users/user/sessions \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Step 2 — Send a query
curl -X POST https://adk-agent-135138907357.us-central1.run.app/run \
  -H "Content-Type: application/json" \
  -d "{
    \"app_name\": \"adk_agent\",
    \"user_id\": \"user\",
    \"session_id\": \"$SESSION_ID\",
    \"new_message\": {
      \"role\": \"user\",
      \"parts\": [{\"text\": \"What are the top rated restaurants in Nashville?\"}]
    }
  }"
```

### Sample queries to try
- `What are the top rated restaurants in Nashville?`
- `Find me Italian restaurants in Philadelphia`
- `Find restaurants with free WiFi in Philadelphia`

---

## Project Structure
```
flavourfind/
├── prepare_data.py              # Cleans CSV and uploads to BigQuery
├── mcp_toolbox/
│   ├── tools.yaml               # 3 MCP tool definitions
│   └── Dockerfile               # MCP Toolbox container
├── adk_agent/
│   ├── agent.py                 # ADK LlmAgent definition
│   └── __init__.py
└── adk_agent_deploy/
    ├── Dockerfile               # ADK Agent container
    ├── requirements.txt
    └── adk_agent/
        ├── agent.py
        └── __init__.py
```

---

## Dataset

Cleaned Yelp Open Dataset — 34,987 active restaurant businesses across the US.

**Columns:** `business_id`, `name`, `city`, `state`, `stars`, `review_count`, `categories`, `wifi_status`

Source: [Kaggle — Cleaned Yelp Dataset: Restaurants & Reviews](https://www.kaggle.com/datasets/ranjulajayarathna/cleaned-yelp-dataset-restaurants-and-reviews)

---

## Tech Stack

- [Google ADK](https://google.github.io/adk-docs/) — Agent Development Kit
- [MCP Toolbox for Databases](https://github.com/googleapis/genai-toolbox) — MCP server for BigQuery
- [Google BigQuery](https://cloud.google.com/bigquery) — Data warehouse
- [Vertex AI](https://cloud.google.com/vertex-ai) — Gemini 2.0 Flash LLM
- [Cloud Run](https://cloud.google.com/run) — Serverless container deployment
