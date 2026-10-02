import base64,json,re,httpx
from app.config import get_settings
RULES='''You are PocketSmart AI, a budget-aware recommendation assistant. Return ONLY valid JSON. Never claim live availability, stock, reviews or exact live prices. Prices are estimates unless a real marketplace API is connected. Stay within the total budget. Use platform names only from Amazon, Flipkart, IKEA, Swiggy, Zomato, OYO. Schema: {"title":"","summary":"","budget":0,"allocation":{},"recommendations":[{"name":"","category":"","estimated_price":0,"quantity":1,"platform":"Amazon","search_query":"","reason":"","tips":""}],"warnings":[]}'''
class GeminiService:
 async def generate(self,prompt,image_bytes=None,mime_type=None):
    s=get_settings()
    if not s.gemini_api_key: raise RuntimeError("GEMINI_API_KEY is not configured")
    parts=[{"text":RULES+"\nUSER REQUEST:\n"+prompt}]
    if image_bytes: parts.append({"inline_data":{"mime_type":mime_type or "image/jpeg","data":base64.b64encode(image_bytes).decode()}})
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{s.gemini_model}:generateContent"
    payload={"contents":[{"role":"user","parts":parts}],"generationConfig":{"temperature":0.35,"responseMimeType":"application/json"}}
    async with httpx.AsyncClient(timeout=60) as c:
        r=await c.post(url,params={"key":s.gemini_api_key},json=payload); r.raise_for_status(); d=r.json()
    text="".join(p.get("text","") for p in d.get("candidates",[])[0].get("content",{}).get("parts",[]))
    text=re.sub(r'^```(?:json)?\s*|\s*```$','',text.strip())
    try:return json.loads(text)
    except Exception:
        a,b=text.find("{"),text.rfind("}"); return json.loads(text[a:b+1])
