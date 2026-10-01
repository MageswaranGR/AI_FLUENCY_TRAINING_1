import ast,operator,os,re,requests
_OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow,ast.USub:operator.neg}
def _evaluate(node):
 if isinstance(node,ast.Constant) and isinstance(node.value,(int,float)): return node.value
 if isinstance(node,ast.BinOp) and type(node.op) in _OPS: return _OPS[type(node.op)](_evaluate(node.left),_evaluate(node.right))
 if isinstance(node,ast.UnaryOp) and type(node.op) in _OPS: return _OPS[type(node.op)](_evaluate(node.operand))
 raise ValueError("Unsupported expression")
def calculator(expression:str)->str:
 try: return str(_evaluate(ast.parse(expression,mode="eval").body))
 except Exception as e: return f"Calculator error: {e}. Use numbers and + - * / ** ( )."
TAG=re.compile(r"<(script|style)[^>]*>.*?</\1>|<[^>]+>",re.S|re.I); SPACES=re.compile(r"\s+")
def read_webpage(url:str,max_chars:int=2000)->str:
 try:
  if url.startswith(("http://","https://")):
   r=requests.get(url,timeout=10,headers={"User-Agent":"AgenticAI-Lab/1.0"}); r.raise_for_status(); raw=r.text
  elif os.path.exists(url):
   with open(url,encoding="utf-8",errors="ignore") as f: raw=f.read()
  else: return f"Read error: {url!r} is not a URL and no such file exists."
 except Exception as e: return f"Read error: {type(e).__name__}: {e}"
 text=SPACES.sub(" ",TAG.sub(" ",raw)).strip()
 return text if len(text)<=max_chars else text[:max_chars]+" ... [truncated]"
TOOLS=[{"type":"function","function":{"name":"calculator","description":"Safely calculate basic arithmetic.","parameters":{"type":"object","properties":{"expression":{"type":"string"}},"required":["expression"]}}},{"type":"function","function":{"name":"read_webpage","description":"Read a web page or local HTML/text file.","parameters":{"type":"object","properties":{"url":{"type":"string"}},"required":["url"]}}}]
TOOL_FUNCTIONS={"calculator":calculator,"read_webpage":read_webpage}