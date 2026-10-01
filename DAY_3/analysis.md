# Day 3 Analysis — ReAct Agent Failure Handling

**Student:** Dineshkumar K
**Program:** B.Tech Artificial Intelligence & Data Science

## 1. Objective
The task was to build a ReAct agent in plain Python using a safe calculator and a web-page/local-file reader, deliberately test failure modes, and improve the agent with safety guards.

## 2. Agent Design
The agent follows a Reason → Act → Observe loop. The model receives tool schemas, chooses a tool when needed, Python executes it, and the result is returned to the model. The loop stops when a final answer is produced or a limit is reached.

## 3. Tools
The `calculator` performs basic arithmetic without `eval()`. The `read_webpage` tool reads a local HTML/text file or HTTP/HTTPS page, removes HTML tags, and limits the returned text.

## 4. Normal Tests
Known expected calculations from `notice.html` are:
- CS101 + AI202 after 10% scholarship: `(12000 + 18000) × 0.9 = Rs. 27,000`
- All three courses plus hostel laboratory charge: `12000 + 18000 + 15000 + 4500 = Rs. 49,500`
- 15% of AI202: `18000 × 0.15 = Rs. 2,700`

Record actual step counts and traces from the terminal.

## 5. Failure Modes
### Repeating Tool Call
`fees.html` does not exist. The unguarded agent can repeat the same failed read until its step limit. The fixed agent counts identical tool name/argument pairs and stops after the repeat threshold.

### Unknown / Hallucinated Tool
A model can request a tool not present in the registry. The safe `.get()` lookup returns an error message instead of crashing. `unsafe_lookup_demo.py` demonstrates that `TOOL_FUNCTIONS[name]` raises `KeyError`.

### Context Overflow
`big.html` contains a large attendance table. Very large tool output can consume excessive context. The fixed agent limits each observation and also applies a character budget.

## 6. Guards
| Guard | Purpose |
|---|---|
| Repeat detection | Stops repeated identical calls |
| `MAX_TOOL_CHARS` | Limits one observation |
| `CHAR_BUDGET` | Limits total content sent during a run |
| `max_steps` | Final loop stopping condition |

## 7. Actual Observations
Fill these from your own terminal results; do not invent them.

| Test | Observation |
|---|---|
| Merit scholarship total | TODO |
| Hostel student total | TODO |
| 15% of AI202 | TODO |
| Welcome message | TODO |
| Repeating loop | TODO |
| Unknown tool | TODO |
| Context overflow | TODO |

## 8. Conclusion
The experiment demonstrates that a ReAct loop needs defensive controls as well as tool use. Repeat detection, tool validation, output limits, character budgets and maximum-step limits help prevent unproductive loops, crashes and excessive context. The fixed agent keeps the ReAct structure while adding these safeguards.