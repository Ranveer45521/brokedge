from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calculate")
async def calculate(data: Request):
    payload = await data.json()

    broker = payload["broker"]
    buy = float(payload["buy"])
    sell = float(payload["sell"])
    qty = int(payload["quantity"])
    order_type = payload["orderType"]

    turnover = (buy + sell) * qty

    brokerage = 0
    if broker in ["zerodha", "upstox", "groww", "angelone"]:
        brokerage = min(turnover * (0.0003 if order_type == "intraday" else 0.0003), 40)
    elif broker == "icici":
        brokerage = max(turnover * 0.005, 35)

    stt = sell * qty * (0.001 if order_type == "delivery" else 0.00025)
    exchange = turnover * 0.0000325
    sebi = turnover * 0.0000015
    gst = 0.18 * (brokerage + exchange)
    total_charges = brokerage + stt + exchange + sebi + gst
    pnl = (sell - buy) * qty - total_charges
    breakeven = total_charges / qty

    return {
        "turnover": round(turnover, 2),
        "brokerage": round(brokerage, 2),
        "stt": round(stt, 2),
        "exchange": round(exchange, 2),
        "sebi": round(sebi, 2),
        "gst": round(gst, 2),
        "totalCharges": round(total_charges, 2),
        "pnl": round(pnl, 2),
        "breakeven": round(breakeven, 2),
    }
