import json
from config import client,MODEL,banner
from my_tools import TOOLS,TOOL_FUNCTIONS
MAX_TOOL_CHARS=1500; CHAR_BUDGET=30000; REPEAT_THRESHOLD=3
SYSTEM_PROMPT=("You are a college assistant. Use read_webpage to read any page or file the user mentions, and use calculator for arithmetic. Never guess a number that should come from a page. If no tool is needed, answer directly.")
def agent(question,max_steps=6,verbose=True):
 messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":question}]; seen_calls={}; chars_sent=0
 for step in range(1,max_steps+1):
  chars_sent+=sum(len(str(m.get("content",""))) for m in messages)
  if chars_sent>CHAR_BUDGET: return f"Stopped: character budget exceeded ({chars_sent} characters sent)."
  response=client.chat.completions.create(model=MODEL,messages=messages,tools=TOOLS,temperature=0); message=response.choices[0].message
  if not message.tool_calls: return (message.content or "").strip()
  messages.append({"role":"assistant","content":message.content or "","tool_calls":[{"id":c.id,"type":"function","function":{"name":c.function.name,"arguments":c.function.arguments}} for c in message.tool_calls]})
  for call in message.tool_calls:
   name=call.function.name; args={}
   try: args=json.loads(call.function.arguments or "{}")
   except json.JSONDecodeError as e: result=f"Argument error: {e}. Send valid JSON."
   else:
    fn=TOOL_FUNCTIONS.get(name); result=(f"Unknown tool: {name}. Available: {list(TOOL_FUNCTIONS)}" if fn is None else fn(**args))
   result=str(result); sig=(name,json.dumps(args,sort_keys=True)); seen_calls[sig]=seen_calls.get(sig,0)+1
   if seen_calls[sig]>=REPEAT_THRESHOLD: return f"Stopped: the tool {name} was called {REPEAT_THRESHOLD} times with the same arguments and no progress was made. Last result: {result[:200]}"
   if len(result)>MAX_TOOL_CHARS: result=result[:MAX_TOOL_CHARS]+" ... [observation truncated]"
   if verbose: print(f"step {step}: {name}({args}) -> {result[:200]}")
   messages.append({"role":"tool","tool_call_id":call.id,"content":result})
 return "Stopped: maximum steps reached without a final answer."
if __name__=="__main__":
 banner("MY AGENT (GUARDS ON)")
 for q in ["Read notice.html and tell me the total fee for CS101 and AI202 after the merit scholarship.","Read fees.html and tell me the fee for CS101.","Read big.html and tell me how many students are listed."]:
  print("\nQ:",q); print("A:",agent(q))