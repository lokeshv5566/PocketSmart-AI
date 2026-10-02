import json
from app.services.gemini_service import GeminiService
from app.services.platform_service import enrich

def normalize(r,typ,budget):
    rec=[]
    for x in r.get("recommendations",[]) if isinstance(r.get("recommendations",[]),list) else []:
        if isinstance(x,dict): rec.append({"name":str(x.get("name","Suggested option")),"category":str(x.get("category","General")),"estimated_price":float(x.get("estimated_price",0) or 0),"quantity":max(1,int(x.get("quantity",1) or 1)),"platform":str(x.get("platform","Amazon")),"search_query":str(x.get("search_query",x.get("name","product"))),"reason":str(x.get("reason","")),"tips":str(x.get("tips",""))})
    return {"title":str(r.get("title",typ.title()+" Budget Plan")),"summary":str(r.get("summary","Budget-aware recommendations generated.")),"budget":float(budget),"allocation":{str(k):float(v) for k,v in (r.get("allocation",{}) if isinstance(r.get("allocation",{}),dict) else {}).items()},"recommendations":enrich(rec),"warnings":[str(x) for x in r.get("warnings",[]) if x],"source":"Gemini AI"}
def home_f(d):
    b=d["budget"]; n=len(d["items"]); a={x["category"]:round(b/n,2) for x in d["items"]}; rec=[]
    for x in d["items"]: rec.append({"name":f"Budget-friendly {x['category']}","category":x["category"],"estimated_price":round(b/n/max(x["quantity"],1),2),"quantity":x["quantity"],"platform":"IKEA" if "furniture" in x["category"].lower() else "Amazon","search_query":f"{d['style']} {x['category']}","reason":"Fits the requested style and allocated budget.","tips":"Compare dimensions, warranty and reviews."})
    return {"title":f"{d['room_type']} budget plan","summary":"Fallback plan because AI service was unavailable.","budget":b,"allocation":a,"recommendations":enrich(rec),"warnings":["AI unavailable; prices are illustrative estimates."],"source":"Fallback"}
def party_f(d):
    b=d["budget"]; a={"Food & catering":round(b*.45,2),"Decoration":round(b*.20,2),"Venue":round(b*.25,2),"Entertainment":round(b*.10,2)}
    rec=[{"name":f"{d['event_type']} catering package","category":"Food & catering","estimated_price":a["Food & catering"],"quantity":1,"platform":"Swiggy","search_query":f"{d['event_type']} catering {d['guests']} guests","reason":"Food allocation reflects guest count.","tips":"Confirm per-person pricing and delivery charges."},{"name":f"{d['event_type']} decoration","category":"Decoration","estimated_price":a["Decoration"],"quantity":1,"platform":"Amazon","search_query":f"{d['event_type']} party decorations","reason":"Controlled decoration spending preserves the total budget.","tips":"Prefer reusable decorations."},{"name":f"Venue search in {d['city']}","category":"Venue","estimated_price":a["Venue"],"quantity":1,"platform":"OYO","search_query":f"party venue {d['city']}","reason":"Venue is separately budgeted.","tips":"Ask about taxes, deposits and cancellation."}]
    return {"title":f"{d['event_type']} party budget plan","summary":"Fallback allocation because AI service was unavailable.","budget":b,"allocation":a,"recommendations":enrich(rec),"warnings":["AI unavailable; vendor prices are illustrative."],"source":"Fallback"}
def jewelry_f(d):
    b=d["budget"]; rec=[{"name":f"{d['style']} {d['metal']} jewelry set","category":"Main piece","estimated_price":round(b*.65,2),"quantity":1,"platform":"Amazon","search_query":f"{d['style']} {d['metal']} jewelry {d['occasion']}","reason":"Matches style and occasion.","tips":"Check material, dimensions and return policy."},{"name":f"Matching {d['style']} accessory","category":"Matching piece","estimated_price":round(b*.35,2),"quantity":1,"platform":"Flipkart","search_query":f"matching {d['style']} jewelry accessory","reason":"Reserves budget for coordination.","tips":"Match accessory scale and color with the outfit."}]
    return {"title":f"{d['occasion']} jewelry plan","summary":"Fallback style-aware starter set.","budget":b,"allocation":{"Main piece":round(b*.65,2),"Matching piece":round(b*.35,2)},"recommendations":enrich(rec),"warnings":["AI unavailable; image analysis was not performed."],"source":"Fallback"}
async def generate_home(d):
    try:return normalize(await GeminiService().generate(f"Create a home interior plan. Budget ₹{d['budget']}; room {d['room_type']}; style {d['style']}; items {json.dumps(d['items'])}. Keep estimated spend within budget."),"home",d["budget"])
    except Exception:return home_f(d)
async def generate_party(d):
    try:return normalize(await GeminiService().generate(f"Create a party plan. Budget ₹{d['budget']}; guests {d['guests']}; event {d['event_type']}; venue {d['venue']}; city {d['city']}; preferences {d['preferences']}. Allocate catering, decoration, venue and entertainment."),"party",d["budget"])
    except Exception:return party_f(d)
async def generate_jewelry(d,image_bytes=None,mime_type=None):
    try:return normalize(await GeminiService().generate(f"Create jewelry recommendations. Budget ₹{d['budget']}; occasion {d['occasion']}; style {d['style']}; metal {d['metal']}; outfit {d['outfit_description']}. Analyze attached outfit image only for broad color/style/aesthetic; do not identify the person.",image_bytes,mime_type),"jewelry",d["budget"])
    except Exception:return jewelry_f(d)
