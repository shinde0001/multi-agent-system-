# 📖 Multi-Agent Book Writer

A DAG-orchestrated, multi-agent AI system designed to automatically plan, research, write, edit, and fact-check a complete book using real, verified citations from the internet.

## 🌟 Architecture Overview

This project uses a **Centralized Orchestrator** pattern instead of peer-to-peer agent communication. Every agent has a strict contract (using Pydantic), and the Orchestrator manages the state machine, routing, and revision loops. This ensures determinism, prevents runaway loops, and makes the pipeline highly debuggable.

### The 5 Agents:
1. **🗺️ Planner Agent:** Reads the book brief and generates a structured 3-chapter outline with specific data points that need to be researched.
2. **🔍 Researcher Agent:** Uses DuckDuckGo (`ddgs`) to search the live web and `trafilatura` to scrape article content. Uses the LLM to extract verified facts and verbatim quotes.
3. **✍️ Writer Agent:** Drafts flowing prose (600-900 words per chapter) incorporating the researched facts with inline citations `[1]`.
4. **📝 Editor Agent:** Checks the draft against strict rules (tone, length, no bullet points, required headers). Bounces it back to the writer if it fails.
5. **✅ Fact-Checker Agent:** Re-fetches every URL cited in the text and uses the LLM to verify that the source *actually* supports the claim made by the writer.

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **LLM:** Google Gemini 3.5 Flash (via `google-genai` SDK)
- **Contracts/Validation:** Pydantic v2
- **Web Search:** DuckDuckGo Search (`ddgs`) - 100% free, no API key needed
- **Web Scraping:** Trafilatura
- **CLI/UI:** Rich (for beautiful terminal output)

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Your API Key
Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
Open the `.env` file in the root directory and add your key:
```env
GEMINI_API_KEY=AIzaSyYourKeyHere...
```

### 3. Run the System
```bash
python3 main.py
```

### 4. Interactive Book Setup
When you run the script, the CLI will ask if you want to use the default book brief (about UPI in India). If you select `n`, it will prompt you for:
- **Topic/Title:** E.g., "The History of Drones in Agriculture"
- **Target Audience:** E.g., "5-year old children" or "PhD Robotics Engineers"
- **Tone:** E.g., "Funny and sarcastic" or "Highly academic"

**Why are these needed?**
The *Audience* instructs the **Planner** on how technical the chapters should be. The *Tone* instructs the **Editor** to act as a strict gatekeeper, rejecting drafts from the Writer if they sound too boring or robotic. These variables flow through the entire DAG to guarantee a unique, human-sounding book.

### 5. View the Output
Because the system runs on the Gemini Free Tier (which limits requests to 1500 per day for the `flash-lite` model), the agents are programmed with a 15-second rate-limiting delay to prevent burst limits. 
The entire process takes about **5-10 minutes** to run. 

Once complete, your book will be saved to:
`output/book.md`

---

## 🧠 Why This Architecture? (Engineering Decisions)

- **Centralized over P2P:** Agents talking directly to each other often hallucinate tasks or get stuck in infinite loops. The centralized orchestrator acts as a "Quality Gate" supervisor.
- **Pydantic Contracts:** By forcing the LLM to output strict JSON schemas, we can validate the data programmatically *before* passing it to the next agent.
- **Sequential Processing:** We process Chapter 1 completely (Research → Write → Edit → Check) before moving to Chapter 2, allowing later chapters to maintain tonal consistency.
- **Real Tooling:** LLMs cannot browse the internet reliably on their own. We use pure Python tools (`ddgs` and `trafilatura`) to do the heavy lifting of fetching real HTML, and only use the LLM to *read* the extracted text. This eliminates hallucinated URLs.
