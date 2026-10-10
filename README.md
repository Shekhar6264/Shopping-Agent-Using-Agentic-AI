
# 🛒 Shopping Agent Using Agentic AI

An exploration of **Agentic AI, Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), tool calling, multimodal AI, and AI safety** using Python and the LangChain ecosystem.

This repository contains hands-on experiments and projects developed while learning how to build AI applications that can interact with tools, retrieve information, process documents, and support user-facing workflows.

## 🚀 Projects and Modules

| Module | Description |
|---|---|
| `project_shopping_agent/` | Shopping assistant with a Streamlit interface, product-related functionality, and review support. |
| `simple_agent/` | Product query agent demonstrating tool usage and agent workflows. |
| `simple_llm_calling/` | Fundamentals of calling LLMs from Python. |
| `rag/` | Retrieval-Augmented Generation (RAG) experiments using documents. |
| `vector_db/` | Experiments with vector databases and semantic search concepts. |
| `multi_modal/` | Multimodal AI experiments involving image inputs. |
| `health_analysis/` | Experiments with AI-assisted analysis of blood-work information. |
| `guardials/` | Experiments with guardrails and handling sensitive information. |
| `eval/` | Evaluation-related scripts and agent experiments. |

## 🧰 Tech Stack

- **Language:** Python
- **LLM Providers:** Groq and Google AI, where configured
- **AI Frameworks:** LangChain and related agent tooling
- **Interface:** Streamlit
- **Retrieval:** RAG and vector-search experiments
- **Development Tools:** Jupyter Notebook, Git, GitHub, and `uv`

## ✨ Key Learning Areas

- Connecting Python applications to large language models
- Building tool-enabled AI agents
- Retrieving product information and working with reviews
- Implementing document-based question answering
- Exploring multimodal inputs
- Applying privacy-oriented guardrails
- Experimenting with agent evaluation

## 📁 Repository Structure

```text
Shopping-Agent-Using-Agentic-AI/
├── eval/
├── guardials/
├── health_analysis/
├── multi_modal/
├── project_shopping_agent/
│   ├── app.py
│   ├── shopping_agent.py
│   ├── reviews_api.py
│   └── setup_db.py
├── rag/
├── simple_agent/
├── simple_llm_calling/
├── src/
├── vector_db/
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Shekhar6264/Shopping-Agent-Using-Agentic-AI.git
cd Shopping-Agent-Using-Agentic-AI
```

### 2. Install dependencies

Install Python and [uv](https://docs.astral.sh/uv/) if you haven't already.

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root and add the API keys required by the specific module you want to run.

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
```

Only add the variables required by your application. Some modules may use different variable names.

**Security:** Never commit `.env` or real API keys to GitHub. Keep `.env` in `.gitignore` and share only placeholder values in `.env.example`.

### 4. Run the shopping agent

```bash
uv run streamlit run project_shopping_agent/app.py
```

If your project uses a locally activated virtual environment, you can also run:

```bash
streamlit run project_shopping_agent/app.py
```

Follow the terminal output to open the Streamlit application in your browser.

## 🔐 Security and Privacy

- API keys should be stored in environment variables.
- Never publish passwords, access tokens, or private credentials.
- Review notebooks and datasets before making them public.
- Avoid publishing personal or sensitive health information.

## 🗺️ Future Improvements

- Improve product discovery and recommendation workflows.
- Add more robust tool execution and error handling.
- Expand agent evaluation and testing.
- Improve the user interface and documentation.
- Explore multi-step agent workflows and persistent memory.

## 👨‍💻 Author

**Shekhar Jamalpuri**

Computer Science Engineering Student | Exploring Agentic AI, LLM Applications, and Software Development

- GitHub: [@Shekhar6264](https://github.com/Shekhar6264)
- Portfolio: [Visit my portfolio](https://myportfolio-cqn8.onrender.com/)

---

⭐ If you find this repository useful, consider giving it a star!
