# 💰 Smart Personal Finance Assistant

A simple **Agentic AI-powered Personal Finance Assistant** built as part of my learning journey in AI Agents, LLMs, and Python.

The project demonstrates how an AI agent can understand a user's financial query, decide whether a tool is required, execute the appropriate tool, use memory, and generate a response.

---

## 🖼️ Agent Architecture

![Smart Personal Finance Assistant](images/smart%20finance%20assistant%20image.png)

---

## 🚀 Features

- 💰 Expense calculations using a dedicated calculator tool
- 📚 Budgeting guidance from a local JSON knowledge source
- 🧠 Session/conversation memory
- 💾 Persistent user preferences
- 🔧 LLM-driven tool selection
- 🚫 Missing-data and error handling
- 🔍 Simple agent execution tracing

---

## 🧠 How It Works

The basic agent workflow is:

**User Request → Agent Runtime → LLM → Tool Decision → Tool Execution → Memory → Final Response**

The LLM interprets the user's request and determines what action is required.

Depending on the request, the agent can:

1. Use the **Expense Calculator**
2. Retrieve information using the **Budget Guidance Tool**
3. Save a user preference
4. Retrieve previously saved preferences
5. Respond without using a tool when no tool is required

This demonstrates the separation between:

- **LLM → reasoning and decision making**
- **Tools → performing specific actions**
- **Memory → maintaining useful context**

---

## 🛠️ Technologies Used

- Python
- OpenAI API
- LangChain
- LangGraph
- JSON
- Git
- GitHub

---

## 📁 Project Structure

```text
smart_personal_finance_assistant/
│
├── data/
│   ├── budget_guidance.json
│   └── profile_memory.json
│
├── images/
│   └── smart finance assistant image.png
│
├── agent_app.py
├── memory_store.py
├── tools.py
├── requirements.txt
├── .gitignore
└── README.md
```

> The `.env` file and Python virtual environment are excluded from GitHub using `.gitignore`.

---

## 🔧 Agent Tools

### 💰 Expense Calculator

Performs calculations such as:

- Total
- Percentage
- Difference

### 📚 Budget Guidance

Retrieves local budgeting guidance for categories such as:

- Food
- Travel
- Shopping
- Entertainment
- Bills

### 💾 Memory Tools

The agent can:

- Save user spending preferences
- Retrieve saved preferences
- Maintain conversation context during a session

---

## ▶️ Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/NSKfincode28/smart-personal-finance-assistant.git
```

### 2. Move into the project folder

```bash
cd smart-personal-finance-assistant
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file in the project folder and add:

```text
OPENAI_API_KEY=your_openai_api_key
```

**Never upload your actual API key to GitHub.**

### 5. Run the assistant

```bash
python agent_app.py
```

---

## 💡 Example

A user might ask:

> I spent ₹10,000 on food out of ₹50,000 in total expenses. What percentage went towards food?

The agent can identify that an exact calculation is required, call the **Expense Calculator**, receive the result, and use it to formulate its final response.

---

## 🔭 Future Scope

The prototype could be extended with:

- Automated expense tracking
- Database integration
- Financial goal tracking
- Notifications
- Richer long-term memory
- Additional financial tools
- Integration with financial data sources
- Finance and FP&A automation workflows

---

## 🎯 Learning Objective

This project was developed as a learning exercise to understand:

**Agentic AI • LLMs • Tool Calling • Agent Workflows • Session Memory • Persistent Memory • Structured Execution**

This is a teaching prototype and does not connect to bank accounts or provide professional financial advice.