# AI-Scheduling-Assistant

A sophisticated AI-powered meeting scheduling system that autonomously handles calendar coordination, conflict resolution, and meeting organization through natural language processing and intelligent time slot selection.

## Features

- 🤖 Natural language processing of meeting requests
- 📅 Automatic calendar conflict resolution
- 🔄 Google Calendar integration
- 🌐 RESTful API endpoints
- 👥 Multi-participant support
- ⚡ Intelligent time slot selection
- ⏱️ Custom duration handling
- 📍 Location and virtual meeting support

## Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant.git
cd ai-scheduler
```

2. **Set up environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure:**
- Create `.env` file with required variables
- Set up Google Calendar authentication
- Create `Keys` directory for tokens

#### Why Agentic AI? 
Traditional scheduling tools rely on rule-based automation or human input. Your solution should go further by: 
- Reasoning like a human assistant (e.g., prioritizing attendees, resolving conflicts).
- Acting independently (e.g., sending follow-ups, adjusting for time zones).
- Learning from user preferences (e.g., preferred times, recurring meetings). 


#### Setup & Requirements:
- Tools/APIs Needed: LLM ( vLLM server running on MI300 GPU). 
- Calendar APIs (Google Calendar). 
- Framework – May use License free tools & packages 
- Development Environment: Python

----------------

### To access MI300 Instance, follow the steps as mentioned below :

<img width="809" height="857" alt="{E739B41B-9914-45A1-8413-778E28C7F3E6}" src="https://github.com/user-attachments/assets/3b9d68c7-f994-486b-8734-ff61648bb192" />


----------------

### Prerequisite : 

##### Run the below command in your Notebook Terminal to update the scripts. 
```
git clone https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant.git
cp -r AI-Scheduling-Assistant/* ./
```
-------------

### Extracting Google Calendar Events :
#### The Notebook demonstrates how to programmatically retrieve and process Google Calendar events for a given user and date range.
#### You will be provided with Google Auth Tokens to pull Google Calendar Events.

##### Key Steps:
- Authentication: Load user credentials from a token file.
- API Call: Fetch events between specified start/end dates using the Google Calendar API.
- Data Processing: Extract event details (start/end times, attendees) and structure them into a clean format.
- Output: Return a list of events with attendee counts and time slots.

#### Follow the notebook for example usage : [Calendar_Event_Extraction](https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/Calendar_Event_Extraction.ipynb)

----------------

### Setting-Up vLLM Server with Large Language Models : 

vLLM is an open-source library designed to deliver high throughput and low latency for large language model (LLM) inference. It optimizes text generation workloads by efficiently batching requests and making full use of GPU resources, empowering developers to manage complex tasks like code generation and large-scale conversational AI.

#### Start the vLLM server with DeepSeek LLM 7B Chat Model

Open a new tab in this Jypyter server, click on the terminal icon to open a new terminal, then copy the following command to launch the vLLM server:

```bash
HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/deepseek-ai/deepseek-llm-7b-chat \
        --gpu-memory-utilization 0.9 \
        --swap-space 16 \
        --disable-log-requests \
        --dtype float16 \
        --max-model-len 2048 \
        --tensor-parallel-size 1 \
        --host 0.0.0.0 \
        --port 3000 \
        --num-scheduler-steps 10 \
        --max-num-seqs 128 \
        --max-num-batched-tokens 2048 \
        --max-model-len 2048 \
        --distributed-executor-backend "mp"
```
#### For setting up vLLM server with DeepSeek Model & usage, please follow : [vLLM_Inference_Servering_DeepSeek](https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/vLLM_Inference_Servering_DeepSeek.ipynb)

#### Start the vLLM server with Meta-Llama-3.1-8B-Instruct Model

Open a new tab in this Jypyter server, click on the terminal icon to open a new terminal, then copy the following command to launch the vLLM server:

```bash
HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/meta-llama/Meta-Llama-3.1-8B-Instruct \
        --gpu-memory-utilization 0.3 \
        --swap-space 16 \

## Detailed Setup Guide

### Prerequisites

- Python 3.8+
- Google Calendar API access
- vLLM server access (for AI processing)

### Installation Steps

1. **Create and configure environment file:**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_api_key
   FLASK_HOST=0.0.0.0
   FLASK_PORT=5000
   DEFAULT_TIMEZONE=Asia/Kolkata
   ```

2. **Set up Google Calendar Authentication:**
   - Create project in Google Cloud Console
   - Enable Google Calendar API
   - Create OAuth 2.0 credentials
   - Save credentials in `Keys` directory
   - Follow `GoogleAuth.md` for detailed steps

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### API Usage

#### Schedule Meeting Endpoint
POST `/schedule`
```json
{
    "Request_id": "unique_id",
    "Datetime": "2025-07-17T14:30:00",
    "Location": "Conference Room A",
    "From": "organizer@example.com",
    "Attendees": [
        {"email": "attendee1@example.com"},
        {"email": "attendee2@example.com"}
    ],
    "Subject": "Project Review Meeting",
    "Duration_mins": "60"
}
```

#### Debug Calendar Events
GET `/calendar_events?user=email@example.com&start=2025-07-17T00:00:00&end=2025-07-17T23:59:59`

### Directory Structure
```
ai-scheduler/
├── Agent/             # AI agent implementation
├── utils/             # Utility functions
├── tests/             # Test cases
├── app.py            # Main Flask application
├── config.py         # Configuration
└── requirements.txt  # Dependencies
```

### Testing
```bash
python -m pytest tests/
```

### Logging
- All operations logged to `scheduler.log`
- Detailed error messages in API responses
- Debug endpoint for calendar events

### Security
- OAuth 2.0 authentication for Google Calendar
- Token-based API authentication
- Secure credential storage
- Environment variable configuration

## License

MIT License - See LICENSE file for details
        --disable-log-requests \
        --dtype float16 \
        --max-model-len 2048 \
        --tensor-parallel-size 1 \
        --host 0.0.0.0 \
        --port 4000 \
        --num-scheduler-steps 10 \
        --max-num-seqs 128 \
        --max-num-batched-tokens 2048 \
        --max-model-len 2048 \
        --distributed-executor-backend "mp"
```

#### For setting up vLLM server with LLama Model & usage, please follow : [vLLM_Inference_Servering_LLaMA](https://gitenterprise.xilinx.com/asirra/AI-Scheduling-Assistant/blob/main/vLLM_Inference_Servering_LLaMA.ipynb)
----------------

### Setting-Up AI Agent :


#### Start the vLLM server with DeepSeek Model

Open a new tab in this Jypyter server, click on the terminal icon to open a new terminal, then copy the following command to launch the vLLM server:

```bash
HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/deepseek-ai/deepseek-llm-7b-chat \
        --gpu-memory-utilization 0.9 \
        --swap-space 16 \
        --disable-log-requests \
        --dtype float16 \
        --max-model-len 2048 \
        --tensor-parallel-size 1 \
        --host 0.0.0.0 \
        --port 3000 \
        --num-scheduler-steps 10 \
        --max-num-seqs 128 \
        --max-num-batched-tokens 2048 \
        --max-model-len 2048 \
        --distributed-executor-backend "mp"
```

#### Sample AI Agent that parse Email Input & Output the Processed JSON
```
class AI_AGENT:
    def __init__(self, client, MODEL_PATH):
        self.base_url = BASE_URL
        self.model_path = MODEL_PATH

    def parse_email(self, email_text):
        response = client.chat.completions.create(
            model=self.model_path,
            temperature=0.0,
            messages=[{
                "role": "user",
                "content": f"""
                Yor are an Agent that helps in scheduling meetings.
                Your job is to extracts Email ID's and Meeting Duration.
                You should return :
                1. List of email id's of participants (comma-separated).
                2. Meeting duration in minutes.
                3. Time constraints (e.g., 'next week').
                If the List of email id's of participants are just names, then append @amd.com at the end and return. 
                Return as json with 'participants', 'time_constraints' & 'meeting_duration'.
                Stricty follow the instructions. Strictly return dict with participents email id's, time constraints & meeting duration in minutes only. 
                Don not add any other instrctions or information. 
                
                Email: {email_text}
                
                """
            }]
        )
        return json.loads(response.choices[0].message.content)
```


#### Follow the Notebook for setting-up an example AI Agent : [Sample_AI_Agent](https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/Sample_AI_Agent.ipynb)

The Notebook demonstrates how to create a simple AI Agent that uses vLLM & OpenAI API to communicate with LLM Model.

----------------

### Inputs & Outputs : 
#### Input JSON : 

The input to your code will be in JSON format in the below structure. 
```
{
    "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
    "Datetime": "09-07-2025T12:34:55",
    "Location": "IIT Mumbai",
    "From": "userone.amd@gmail.com",
    "Attendees": [
        {
            "email": "usertwo.amd@gmail.com"
        },
        {
            "email": "userthree.amd@gmail.com"
        }
    ],
    "Subject": "Agentic AI Project Status Update",
    "EmailContent": "Hi team, let's meet on Thursday for 30 minutes to discuss the status of Agentic AI Project."
}
```

#### Final Output JSON : 
```
{
    "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
    "Datetime": "09-07-2025T12:34:55",
    "Location": "IIT Mumbai",
    "From": "userone.amd@gmail.com",
    "Attendees": [
        {
            "email": "userone.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-17T10:30:00+05:30",
                    "EndTime": "2025-07-17T11:00:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Agentic AI Project Status Update"
                }
            ]
        },
        {
            "email": "usertwo.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-17T10:00:00+05:30",
                    "EndTime": "2025-07-17T10:30:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Team Meet"
                },
                {
                    "StartTime": "2025-07-17T10:30:00+05:30",
                    "EndTime": "2025-07-17T11:00:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Agentic AI Project Status Update"
                }
            ]
        },
        {
            "email": "userthree.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-17T10:00:00+05:30",
                    "EndTime": "2025-07-17T10:30:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Team Meet"
                },
                {
                    "StartTime": "2025-07-17T13:00:00+05:30",
                    "EndTime": "2025-07-17T14:00:00+05:30",
                    "NumAttendees": 1,
                    "Attendees": [
                        "SELF"
                    ],
                    "Summary": "Lunch with Customers"
                },
                {
                    "StartTime": "2025-07-17T10:30:00+05:30",
                    "EndTime": "2025-07-17T11:00:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Agentic AI Project Status Update"
                }
            ]
        }
    ],
    "Subject": "Agentic AI Project Status Update",
    "EmailContent": "Hi team, let's meet on Thursday for 30 minutes to discuss the status of Agentic AI Project.",
    "EventStart": "2025-07-17T10:30:00+05:30",
    "EventEnd": "2025-07-17T11:00:00+05:30",
    "Duration_mins": "30",
    "MetaData": {}
}
```

#### We will send JSONs at Port 5000 & will receive your AI Assistant Response
#### Make sure that your Output strictly follows the specified format. 



