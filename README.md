# Q&A Agent Chatbot with Memory and Web Search

A conversational AI chatbot built with **Streamlit, LangChain, LangGraph, and Groq**. It can maintain conversation context during a running session and search the web when external or up-to-date information is needed.

## Features

- **Conversational interface:** Chat with the assistant through a simple Streamlit UI.
- **Conversation memory:** Uses LangGraph's `MemorySaver` checkpointer and a consistent thread ID to retain context across turns in the active application process.
- **Web search tool:** Integrates Google Serper through `GoogleSerperAPIWrapper`, exposed to the agent as a LangChain tool.
- **LLM-powered responses:** Uses Groq's `openai/gpt-oss-120b` model through `ChatGroq`.
- **Grounded response instructions:** The system prompt encourages the assistant to avoid inventing answers and use search for external or current information.
- **Environment-based secrets:** API keys are loaded from a local `.env` file rather than being hard-coded.

## Tech Stack

- Python 3.11+
- Streamlit
- LangChain
- LangGraph
- Groq API (`langchain-groq`)
- Google Serper API
- `python-dotenv`

## Project Structure

```text
Q_A--agent-main/
├── chatbot/
│   ├── app.py              # Streamlit chatbot application
│   └── test.ipynb          # Notebook for experiments/testing
├── src/
│   └── q_a_agent/
│       └── __init__.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Prerequisites

Before running the app, make sure you have:

- Python 3.11 or later
- A Groq API key
- A Serper API key
- Git (optional, for cloning the repository)

## Setup and Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Q_A--agent-main
```

Replace `<your-repository-url>` with your repository's actual URL.

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a file named `.env` in the project root and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

Get your Groq API key from [Groq Console](https://console.groq.com/keys) and your Serper API key from [Serper](https://serper.dev/).

**Security:** Do not commit `.env` or share API keys publicly. Keep real secrets out of source code and screenshots.

## Run the Application

From the project root, run:

```bash
streamlit run chatbot/app.py
```

Streamlit will print a local URL in the terminal (usually `http://localhost:8501`). Open it in your browser to start chatting.

## How It Works

1. The user submits a message in the Streamlit chat interface.
2. The message is sent to the LangChain agent powered by the Groq chat model.
3. LangGraph's checkpointer retrieves prior conversation state associated with the configured thread ID.
4. When appropriate, the model can call the `web_search` tool, which sends a query to Google Serper.
5. The agent returns a response, and Streamlit displays it while retaining the visible messages in session state.

## Memory and Limitations

- `MemorySaver` stores checkpoints in memory. Conversation state is not durable across application process restarts.
- The current app uses a fixed thread ID (`"1"`) per Streamlit session. For multi-user deployments, use isolated thread IDs and an appropriate persistent storage strategy.
- Web search depends on a valid Serper API key, network access, and the availability/limits of the external service.
- Tool invocation is decided by the model; defining a tool does not guarantee it will be called for every question.
- The quality and freshness of answers depend on the model and the search results it receives.

## Troubleshooting

| Problem | What to check |
|---|---|
| Missing Groq API key | Confirm `GROQ_API_KEY` is set in `.env` and restart Streamlit. |
| Web search fails | Verify `SERPER_API_KEY`, account access, and connectivity. |
| Agent does not search | Ask explicitly to search the web and check the terminal for tool/API errors. |
| Packages cannot be imported | Activate the virtual environment and reinstall `requirements.txt`. |
| Memory seems to reset | Keep the same thread ID and avoid restarting the app process; `MemorySaver` is in-memory only. |

## Future Improvements

- Add a clear-chat/new-conversation control.
- Use unique thread IDs for separate conversations and users.
- Add persistent checkpoint storage for memory across restarts.
- Display tool activity and search sources in the interface.
- Add error handling and automated tests for model and search failures.
- Add deployment instructions and configuration for a hosted environment.

## Contributing

Contributions and suggestions are welcome. You can open an issue to report a bug or propose an improvement, then submit a pull request with your changes.

## License

No license is currently specified. Add a `LICENSE` file before distributing the project under a particular open-source license.

---

Built as a learning project exploring AI agents, conversational memory, and tool-assisted web search.
