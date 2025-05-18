# Simple AI Chatbot
A free and open-source AI chatbot framework that you can deploy on your local system using Chainlit and g4f.
Build your AI chatbot and start chatting in minutes — no API key required!

## 🚀 Features
- Modular framework for building new skills, MCPs, and AI agents
- Backend powered by Chainlit and pre-configured for easy use
- User authentication (register and login)
- Multilingual interface (currently supports Persian and English)
- Persistent chat history
- No limitations or paywalls
- No need for any API keys (e.g. OpenAI, Gemini)
- Always free and open-source

## 🧠 Current Skills
 - Text-based conversation
 - Image generation
 - Skill development
 - Product search & purchase from Torob (available for Iranian users)

>💡 **What is a Skill?** <br>
A "skill" is an extension of the chatbot's capabilities. Think of it like a plugin that adds new functionality — such as image creation, product search, etc. Skills can be used in place of MCPs or AI Agents.

## 📦 Installation
Before you start, make sure Docker is installed on your system.

For Windows & macOS:
Download and install Docker Desktop:<br>
[🔗 Docker installation guide](https://docs.docker.com/engine/install/)

For Debian-based Linux:<br>
Run the following commands in the terminal:
```
sudo apt update
sudo apt upgrade -y
sudo apt install docker-compose
sudo apt install docker-compose-v2
```
>⚠️ If you encounter "permission denied" errors, try using sudo with your commands.

## 💻 Minimum System Requirements
Tested on: Dell 5520 (Intel Core i7-7H, 16GB RAM, Debian-based Linux)

Minimum:
- CPU: 2 cores
- RAM: 2 GB
- Storage: 20 GB
- Internet connection

## ⚙️ Getting Started
### 1. Set up your environment:
Copy the example .env file:

```
cp .env.example .env
```
Edit the `.env` file and update the following fields:

```
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
DATABASE_URL="postgresql+asyncpg://myuser:mypassword@postgres:5432/mydb"
INTERFACE_LANG=fa
CHAINLIT_AUTH_SECRET="your-secret-key"
```
### 2. Start the app:
Run the following command:

```
docker compose up
```
Once the containers are running, access your chatbot at:<br>
🌐 http://localhost:80

> 💡 If port 80 is unavailable, you can change the Nginx port in the `docker-compose.yml` file.

### 🌍 Change Interface Language
To switch between English and Persian, update the `INTERFACE_LANG` field in your `.env` file:

```
INTERFACE_LANG=fa  # or 'en'
```
## 🛠️ Next Steps
Use this repository as a base and start building new skills to share with others.
We plan to release a **developer guide** and **detailed documentation** soon.

## ✅ Project Tasks
 - [] Write developer guide
 - [] Add code documentation
 - [] Develop new skills
 - [] Upload files & support reading datasheets
 - [x] Add register page
 - [x] Create README file
 - [x] Create .env file
 - [x] Release Docker image for frontend

Let me know if you'd like this translated into Persian or want to add badges, screenshots, or a video demo