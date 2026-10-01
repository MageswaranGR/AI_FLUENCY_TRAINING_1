import json
from config import client,MODEL,banner
from my_tools import TOOLS,TOOL_FUNCTIONS
SYSTEM_PROMPT=("You are a college assistant. Use read_webpage to read any page or file the user mentions, and use calculator for arithmetic. Never guess a number that should come from a page. If no tool is needed, answer directly.")
def agent(question,max_steps=6,verbose=True):
 messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":question}]
 for step in range(1,max_steps+1):
  response=client.chat.completions.create(model=MODEL,messages=messages,tools=TOOLS,temperature=0); message=response.choices[0].message
  if not message.tool_calls: return (message.content or "").strip()
  messages.append({"role":"assistant","content":message.content or "","tool_calls":[{"id":c.id,"type":"function","function":{"name":c.function.name,"arguments":c.function.arguments}} for c in message.tool_calls]})
  for call in message.tool_calls:
   name=call.function.name; args={}
   try:
    args=json.loads(call.function.arguments or "{}"); fn=TOOL_FUNCTIONS.get(name)
    result=(f"Unknown tool: {name}. Available: {list(TOOL_FUNCTIONS)}" if fn is None else fn(**args))
   except json.JSONDecodeError as e: result=f"Argument error: {e}. Send valid JSON."
   except Exception as e: result=f"Tool error: {type(e).__name__}: {e}"
   result=str(result)
   if verbose: print(f"step {step}: {name}({args}) -> {result[:200]}")
   messages.append({"role":"tool","tool_call_id":call.id,"content":result})
 return "Stopped: maximum steps reached without a final answer."
if __name__=="__main__":
 banner("MY AGENT (NO GUARDS)")
 for q in ["Read notice.html and tell me the total fee for CS101 and AI202 after the merit scholarship.","Read notice.html. What does a hostel student taking all three courses pay in total, including laboratory charges?","What is 15% of the AI202 fee?","Write a one-line welcome message for new students."]:
  print("\nQ:",q); print("A:",agent(q))