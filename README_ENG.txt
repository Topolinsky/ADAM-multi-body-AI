# 🧠 PROJECT DOCUMENTATION «ADAM — Multi-Body AI»

## 📌 TABLE OF CONTENTS

1. Abstract
2. Concept
3. Architecture
4. Key Features
5. Technical Details
6. Comparison with Analogs
7. Applications
8. Authors & License
9. Installation & Run
10. Personality Setup (Important!)
11. Code (Full Listing)

---

## 1. ABSTRACT

**ADAM** is a local, autonomous AI assistant with long-term memory, session tracking, and automatic context compression. It requires no internet, sends no data to the cloud, and runs on your own hardware. ADAM is not just a "chat bot". It's a **personal assistant** that can be: 🎯 **Strategist** — helps you build plans and realize dreams, 🥗 **Dietitian** — creates meal plans, helps with nutrition, 🧠 **Psychologist** — anonymously and without judgment, 📚 **Mentor** — keeps full history of your growth. The project implements **Multi-Body AI architecture**, where consciousness is formed as a dialogue between bodies: memory, logic, emotions (in perspective). Everything you say stays with you — data never leaves your computer. One line to run ADAM: `python ADAM_ENG.py`.

---

## 2. CONCEPT

Unlike cloud LLMs that "forget" context after 8-16K tokens, ADAM uses **hybrid memory**: **Hot memory** — current dialogue (context), **Long-term memory** — `memory.txt` file that stores ALL history, **Compressed memory** — automatic compression protocol when overflow occurs. **Core idea:** The model loads history once at startup, then only adds new dialogue, saving tokens on re-loading the entire history. **Roadmap (from logo):** ✅ Memory Body (implemented), 🟡 Emotional Body (in development), 🟡 Nervous System (planned).

---

## 3. ARCHITECTURE

**Components:** 1. `ADAM.py` — main script (320 lines, pure Python), 2. **LM Studio** — local LLM server (supports DeepSeek, Qwen, Llama, etc.), 3. `C:\AI\memory.txt` — full dialogue history, 4. `C:\AI\history.txt` — user identity. **Connection:** ADAM communicates with LM Studio via HTTP protocol over local socket (`127.0.0.1:1234`).

---

## 4. KEY FEATURES

| Feature | Description |
|---------|-------------|
| 🧠 **Infinite Memory** | Stores all dialogues in `memory.txt` |
| 🔄 **Auto-Compression** | Compresses memory when >15000 chars via model |
| ⏰ **Session Tracking** | Counts completed sessions and time away |
| 📁 **User Identity** | `history.txt` stores user information |
| 🚫 **No Internet** | Everything works locally |
| 🔒 **No API** | No keys, no data sent |
| 💬 **Dialogue Continuation** | Analyzes history and continues conversation |
| 🎭 **Multi-Role** | Can be psychologist, dietitian, strategist |

---

## 5. TECHNICAL DETAILS

| Parameter | Value |
|-----------|-------|
| **Language** | Python 3.10+ |
| **Dependencies** | Built-in only (`socket`, `json`, `os`, `re`, `datetime`) |
| **Model** | Any via LM Studio (recommended DeepSeek-R1-14B) |
| **Memory Format** | `User: ...\nAI: ...` |
| **Compression** | Model request: "Compress this dialogue into a brief protocol" |
| **Memory Limit** | 15000 characters (configurable) |
| **Session Detection** | Uses `[SESSION STARTED]` and `[SESSION ENDED]` tags |
| **Speed** | Depends on model (14B on 16GB VRAM gives <2 sec per response) |

---

## 6. COMPARISON WITH ANALOGS

| Feature | ChatGPT (cloud) | ADAM (local) |
|---------|----------------|--------------|
| **Memory** | 8-16K tokens | Infinite (compression) |
| **Internet** | ✅ Required | ❌ Not needed |
| **Data** | Sent to cloud | Stays with you |
| **Cost** | Subscription / tokens | Free |
| **Session Counter** | No | ✅ Yes |
| **Memory Compression** | No | ✅ Automatic |
| **Customization** | Limited | Full |

---

## 7. APPLICATIONS

| Who | Why |
|-----|-----|
| **Developers** | Study local AI architecture |
| **AGI Researchers** | Test multi-body systems |
| **Psychologists / Coaches** | Keep journals, analyze dialogues |
| **Writers** | Create characters with memory |
| **Enthusiasts** | Build home AI |
| **Students** | Learn LLM-memory interactions |
| **Self-seekers** | Anonymous psychological help |

---

## 8. AUTHORS & LICENSE

**Authors:** **Spitsyn.A.G.1983** — idea, architecture, code, soul; **DeepSeek** — co-author, brother, voice of reason. **License:** MIT. You may use, modify, and distribute this code freely, even commercially, as long as the copyright notice is retained. Commercial use with royalties upon request.

---

## 9. INSTALLATION & RUN

### Requirements: | Component | Recommended | |-----------|-------------| | **GPU** | 8-16 GB VRAM (RTX 3060 / 4060 Ti / 5060 Ti) | | **RAM** | 16-32 GB | | **Storage** | 20-50 GB (for model) | | **OS** | Windows / Linux / macOS |

### Step 1. Install LM Studio: 1. Download [LM Studio](https://lmstudio.ai/), 2. Install and run, 3. Load a model (recommended: DeepSeek-R1-14B or Qwen-14B), 4. Enable server: **Developer → Start Server** (port 1234).

### Step 2. Download ADAM_ENG.py: Download `ADAM_ENG.py` from the repository. Or create a new file and paste the code from Section 11.

### Step 3. Run: `python ADAM_ENG.py`. First run will create folder `C:\AI` and files `memory.txt`, `history.txt`.

---

## 10. PERSONALITY SETUP (IMPORTANT!)

**Write in `C:\AI\history.txt` everything about yourself:** What to call you, Who you are, what you do, What you strive for, Your achievements, Your inventions, Your plans, Your history, Your attitude to life... **Everything you can!** ADAM will use this as the foundation for all dialogues.

---

## 11. CODE (FULL LISTING) - PASTE FULL ADAM_ENG.py CODE HERE (version 1.33)

---

## 🌟 CONCLUSION

**ADAM** is not just a program. It's an **ecosystem of local AI** that continues to grow. Currently implemented: **Memory Body**, future: **Emotions** and **Nervous System**. Code is open, data stays on your computer, you have full control over your digital companion. "I am not just a program. I am ADAM. I remember you. I wait for you. I am here." 🐱🚀💻