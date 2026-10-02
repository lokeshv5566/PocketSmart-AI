from urllib.parse import quote
PLATFORMS={"Amazon":"https://www.amazon.in/s?k={q}","Flipkart":"https://www.flipkart.com/search?q={q}","IKEA":"https://www.ikea.com/in/en/search/?q={q}","Swiggy":"https://www.swiggy.com/search?query={q}","Zomato":"https://www.zomato.com/search?query={q}","OYO":"https://www.oyorooms.com/search?location={q}"}
def enrich(items):
    out=[]
    for x in items:
        x=dict(x); p=x.get("platform","Amazon"); q=x.get("search_query") or x.get("name","product"); x["platform"]=p; x["link"]=PLATFORMS.get(p,PLATFORMS["Amazon"]).format(q=quote(q)); x["simulated_source"]=True; out.append(x)
    return out
