# 🤖 AI-Scheduling-Assistant

A sophisticated, agentic AI-powered meeting scheduling system that autonomously handles calendar coordination, conflict resolution, and intelligent time slot selection via natural language understanding.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Status: Completed](https://img.shields.io/badge/Status-Completed-brightgreen)
![Built with: Machine Learning](https://img.shields.io/badge/Built%20With-Machine%20Learning-blueviolet)
[![trophy](https://github-profile-trophy.vercel.app/?username=OneTeraByte7&theme=onedark)](https://github.com/ryo-ma/github-profile-trophy)

> ⚡️ This project was built during an **intense invite-only Hackathon hosted by AMD**, aimed at pushing the limits of agentic AI for real-world enterprise applications.

---

## 🚀 Features

- 🧠 Natural language meeting parsing
- 🗓️ Google Calendar integration
- 🔄 Calendar conflict detection & resolution
- 👥 Multi-participant support
- 🕰️ Intelligent time slot selection
- 📍 Location + virtual meeting compatibility
- ⚙️ REST API endpoints
- 💡 Custom duration & time zone handling
- 🔐 OAuth 2.0 & secure credentials

---

## 🧰 Tech Stack

- 🐍 Python 3.8+
- 🌐 Flask REST API
- 📅 Google Calendar API
- ⚙️ vLLM (MI300 GPU) with DeepSeek / Meta-LLaMA models
- 🤖 Agentic AI for task execution

---

## ⚡ Quickstart

```bash
git clone https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant.git
cd AI-Scheduling-Assistant
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Create a .env with:
```bash
  OPENAI_API_KEY=your_api_key
  FLASK_HOST=0.0.0.0
  FLASK_PORT=5000
  DEFAULT_TIMEZONE=Asia/Kolkata
```
##Add Google Calendar credentials to Keys/.

## 🤖 Why Agentic AI?

Unlike traditional schedulers, this assistant:
Reasons: Understands constraints, priorities, and attendee availability
Acts: Chooses slots, initiates rescheduling, sends reminders
Learns: Adapts based on usage patterns (e.g., preferred hours, locations)

## 🛠️ API Example
Schedule Meeting
POST /schedule:
```bash
{
  "Request_id": "123",
  "Datetime": "2025-07-17T14:30:00",
  "Location": "Conference Room A",
  "From": "organizer@example.com",
  "Attendees": [
    {"email": "attendee1@example.com"},
    {"email": "attendee2@example.com"}
  ],
  "Subject": "Project Review",
  "Duration_mins": "60"
}
```

##Calendar Events:
```bash
GET /calendar_events?user=email@example.com&start=YYYY-MM-DDT00:00:00&end=YYYY-MM-DDT23:59:59
```

## 📂 Project Structure:
```bash
AI-Scheduling-Assistant/
├── Agent/                  # AI agent logic
├── utils/                  # Helper functions
├── tests/                  # Pytest test cases
├── app.py                  # Main Flask API
├── config.py               # Env/config handling
├── requirements.txt        # Python dependencies
└── Keys/                   # Auth credentials
```
## 🧪 Testing
```bash
python -m pytest tests/
```

## 🔐 Security:

OAuth 2.0 Google authentication
Tokens and keys stored securely
Environment-variable driven configuration

## 🧠 vLLM Inference Setup
Use MI300-based vLLM with DeepSeek or Meta-LLaMA:
```bash
HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/deepseek-ai/deepseek-llm-7b-chat \
  --gpu-memory-utilization 0.9 \
  --swap-space 16 \
  --host 0.0.0.0 --port 3000 \
  --dtype float16 --max-model-len 2048
```

## 📜 License
This project is licensed under the MIT License © 2025 Soham
Feel free to use, modify, and distribute with proper attribution.
