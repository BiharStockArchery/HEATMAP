import yfinance as yf
from flask import Flask, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import os
import pytz
from datetime import datetime

app = Flask(__name__)

# Enable CORS for the Flask app
CORS(app)

# List of sector-wise stock symbols from NSE
symbols = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS","ACC.NS",
"APLAPOLLO.NS",
"AUBANK.NS",
"AARTIIND.NS",
"ABBOTINDIA.NS",
"ADANIENSOL.NS",
"ADANIENT.NS",
"ADANIGREEN.NS",
"ADANIPORTS.NS",
"ATGL.NS",
"ABCAPITAL.NS",
"ABFRL.NS",
"ALKEM.NS",
"AMBUJACEM.NS",
"ANGELONE.NS",
"APOLLOHOSP.NS",
"APOLLOTYRE.NS",
"ASHOKLEY.NS",
"ASIANPAINT.NS",
"ASTRAL.NS",
"ATUL.NS",
"AUROPHARMA.NS",
"DMART.NS",
"AXISBANK.NS",
"BSOFT.NS",
"BSE.NS",
"BAJAJ-AUTO.NS",
"BAJFINANCE.NS",
"BAJAJFINSV.NS",
"BALKRISIND.NS",
"BANDHANBNK.NS",
"BANKBARODA.NS",
"BANKINDIA.NS",
"BATAINDIA.NS",
"BERGEPAINT.NS",
"BEL.NS",
"BHARATFORG.NS",
"BHEL.NS",
"BPCL.NS",
"BHARTIARTL.NS",
"BIOCON.NS",
"BOSCHLTD.NS",
"BRITANNIA.NS",
"CESC.NS",
"CGPOWER.NS",
"CANFINHOME.NS",
"CANBK.NS",
"CDSL.NS",
"CHAMBLFERT.NS",
"CHOLAFIN.NS",
"CIPLA.NS",
"CUB.NS",
"COALINDIA.NS",
"COFORGE.NS",
"COLPAL.NS",
"CAMS.NS",
"CONCOR.NS",
"COROMANDEL.NS",
"CROMPTON.NS",
"CUMMINSIND.NS",
"CYIENT.NS",
"DLF.NS",
"DABUR.NS",
"DALBHARAT.NS",
"DEEPAKNTR.NS",
"DELHIVERY.NS",
"DIVISLAB.NS",
"DIXON.NS",
"LALPATHLAB.NS",
"DRREDDY.NS",
"EICHERMOT.NS",
"ESCORTS.NS",
"EXIDEIND.NS",
"NYKAA.NS",
"GAIL.NS",
"GMRAIRPORT.NS",
"GLENMARK.NS",
"GODREJCP.NS",
"GODREJPROP.NS",
"GRANULES.NS",
"GRASIM.NS",
"GUJGASLTD.NS",
"GNFC.NS",
"HCLTECH.NS",
"HDFCAMC.NS",
"HDFCBANK.NS",
"HDFCLIFE.NS",
"HFCL.NS",
"HAVELLS.NS",
"HEROMOTOCO.NS",
"HINDALCO.NS",
"HAL.NS",
"HINDCOPPER.NS",
"HINDPETRO.NS",
"HINDUNILVR.NS",
"HUDCO.NS",
"ICICIBANK.NS",
"ICICIGI.NS",
"ICICIPRULI.NS",
"IDFCFIRSTB.NS",
"IPCALAB.NS",
"IRB.NS",
"ITC.NS",
"INDIAMART.NS",
"INDIANB.NS",
"IEX.NS",
"IOC.NS",
"IRCTC.NS",
"IRFC.NS",
"IGL.NS",
"INDUSTOWER.NS",
"INDUSINDBK.NS",
"NAUKRI.NS",
"INFY.NS",
"INDIGO.NS",
"JKCEMENT.NS",
"JSWENERGY.NS",
"JSWSTEEL.NS",
"JSL.NS",
"JINDALSTEL.NS",
"JIOFIN.NS",
"JUBLFOOD.NS",
"KEI.NS",
"KPITTECH.NS",
"KALYANKJIL.NS",
"KOTAKBANK.NS",
"LTF.NS",
"LTTS.NS",
"LICHSGFIN.NS",
"LTIM.NS",
"LT.NS",
"LAURUSLABS.NS",
"LICI.NS",
"LUPIN.NS",
"MRF.NS",
"LODHA.NS",
"MGL.NS",
"M&MFIN.NS",
"M&M.NS",
"MANAPPURAM.NS",
"MARICO.NS",
"MARUTI.NS",
"MFSL.NS",
"MAXHEALTH.NS",
"METROPOLIS.NS",
"MPHASIS.NS",
"MCX.NS",
"MUTHOOTFIN.NS",
"NCC.NS",
"NHPC.NS",
"NMDC.NS",
"NTPC.NS",
"NATIONALUM.NS",
"NAVINFLUOR.NS",
"NESTLEIND.NS",
"OBEROIRLTY.NS",
"ONGC.NS",
"OIL.NS",
"PAYTM.NS",
"OFSS.NS",
"POLICYBZR.NS",
"PIIND.NS",
"PVRINOX.NS",
"PAGEIND.NS",
"PERSISTENT.NS",
"PETRONET.NS",
"PIDILITIND.NS",
"PEL.NS",
"POLYCAB.NS",
"POONAWALLA.NS",
"PFC.NS",
"POWERGRID.NS",
"PRESTIGE.NS",
"PNB.NS",
"RBLBANK.NS",
"RECLTD.NS",
"RELIANCE.NS",
"SBICARD.NS",
"SBILIFE.NS",
"SHREECEM.NS",
"SJVN.NS",
"SRF.NS",
"MOTHERSON.NS",
"SHRIRAMFIN.NS",
"SIEMENS.NS",
"SONACOMS.NS",
"SBIN.NS",
"SAIL.NS",
"SUNPHARMA.NS",
"SUNTV.NS",
"SUPREMEIND.NS",
"SYNGENE.NS",
"TATACONSUM.NS",
"TVSMOTOR.NS",
"TATACHEM.NS",
"TATACOMM.NS",
"TCS.NS",
"TATAELXSI.NS",
"TATAMOTORS.NS",
"TATAPOWER.NS",
"TATASTEEL.NS",
"TECHM.NS",
"FEDERALBNK.NS",
"INDHOTEL.NS",
"RAMCOCEM.NS",
"TITAN.NS",
"TORNTPHARM.NS",
"TRENT.NS",
"TIINDIA.NS",
"UPL.NS",
"ULTRACEMCO.NS",
"UNIONBANK.NS",
"UBL.NS",
"UNITDSPR.NS",
"VBL.NS",
"VEDL.NS",
"IDEA.NS",
"VOLTAS.NS",
"WIPRO.NS",
"YESBANK.NS",
"ZOMATO.NS",
  # Add more symbols as needed
]

# Define the timezone (Indian Standard Time)
IST = pytz.timezone('Asia/Kolkata')

def get_sector_data():
    try:
        # Get the current date and time
        now = datetime.now(IST)

        # Fetch 5 days of minute-level data to get the high, low and previous day's close prices
        data = yf.download(symbols, period="5d", interval="1m")  # 5-day minute-level data

        # Debugging: Print fetched data
        print("Fetched data:\n", data)

        # Check if the data contains 'Adj Close' or 'Close' for accurate price info
        stock_data = data.get('Adj Close', data.get('Close'))

        if stock_data is None or stock_data.empty:
            print("Error: No valid stock data for symbols.")
            return {"error": "No valid stock data available."}

        # Prepare the result data dictionary
        result_data = {}

        # Loop through the stock symbols and calculate data for each
        for symbol in symbols:
            # Get the previous day's closing price (last row in 'Adj Close' or 'Close' column)
            previous_day_close = stock_data[symbol].iloc[-2]  # Previous day's closing price
            
            # Get the current day's last close price (for comparison)
            current_price = stock_data[symbol].iloc[-1]  # Today's most recent price (last row)

            # Calculate the percentage change from the previous day's close price
            percentage_change = ((current_price - previous_day_close) / previous_day_close) * 100

            # Only include the data if it is not NaN
            if not (current_price != current_price or previous_day_close != previous_day_close):
                result_data[symbol] = {
                    "current_price": current_price,
                    "percentage_change": percentage_change
                }

        return result_data

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}

# Define the background task function
def update_sector_data():
    print("Running background task to update sector data...")
    sector_data = get_sector_data()
    print("Sector data updated:", sector_data)

@app.route('/sector-heatmap')
def sector_heatmap():
    sector_data = get_sector_data()

    if "error" in sector_data:
        return jsonify({"status": "error", "message": sector_data["error"]}), 400

    return jsonify({"status": "success", "data": sector_data})

if __name__ == '__main__':
    # Set up the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_sector_data, trigger="interval", seconds=60)  # Run every 60 seconds
    scheduler.start()

    # Ensure Flask is properly shut down with the scheduler
    try:
        port = int(os.environ.get("PORT", 5000))  # Railway provides the port dynamically
        app.run(host='0.0.0.0', port=port, debug=True)  # Use 0.0.0.0 to bind to all network interfaces
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
