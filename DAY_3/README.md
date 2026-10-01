# Day 3 — ReAct Agent From Scratch

**Student:** MAGESWARAN GR

## Setup
```powershell
python -m pip install -r requirements.txt
```
Copy `.env.example` to `.env`. The default setup uses Ollama and `qwen2.5:1.5b`.

Check the model with `ollama list`; if needed run `ollama pull qwen2.5:1.5b`.

## Run
```powershell
python my_agent.py
python my_agent_fixed.py
python unsafe_lookup_demo.py
python make_big_page.py
```

## Files
- `my_tools.py` — calculator, page reader, registry and schemas
- `my_agent.py` — ReAct loop without the three new guards
- `my_agent_fixed.py` — guarded version
- `notice.html` — fee notice
- `big.html` — large attendance page
- `make_big_page.py` — recreates the large page
- `unsafe_lookup_demo.py` — demonstrates unsafe lookup
- `failure_log.md` — actual failure observations
- `observation_table.md` — actual step counts/tool calls
- `analysis.md` — short analysis

Do not upload `.env` or `.venv` to GitHub.