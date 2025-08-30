# Gold Price Prediction App - Data Utilities
# This module contains functions to fetch, prepare, and process market data for gold price prediction.


import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import joblib
import os
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score
from fredapi import Fred

# ------------------ FRED API KEY ------------------
FRED_API_KEY = "d948378e45604ab56ba58e5de8a1bd53"
fred = Fred(api_key=FRED_API_KEY)

# ------------------ MODEL DIRECTORY ------------------
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# ------------------ FETCH MARKET DATA ------------------
symbols = {
    "Gold": "GC=F",
    "SP500": "^GSPC",
    "DowJones": "^DJI",
    "Euro": "EUR=X",
    "EuroStoxx": "^STOXX50E",
    "CrudeOil": "CL=F",
    "Apple": "AAPL",
    "USBonds10Y": "^TNX",
    "USBankETF": "KBE",
    "Platinum": "PL=F",
    "Palladium": "PA=F",
    "GoldMinersETF": "GDX",
    "USOilETF": "USO",
    "USDIndex": "DX-Y.NYB"
}

def fetch_market_data():
    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=365 * 20)
    data_frames = []

    for name, ticker in symbols.items():
        try:
            df = yf.download(ticker, start=start, end=end)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(col).strip() for col in df.columns.values]
            df = df.rename(columns={
                'Open': f'{name}_Open',
                'High': f'{name}_High',
                'Low': f'{name}_Low',
                'Close': f'{name}_Close',
                'Adj Close': f'{name}_AdjClose',
                'Volume': f'{name}_Volume'
            })
            data_frames.append(df)
        except Exception as e:
            print(f"Error fetching {name} ({ticker}): {e}")

    combined_df = pd.concat(data_frames, axis=1)
    combined_df.dropna(inplace=True)

    if 'Gold_Close' in combined_df.columns and 'Euro_Close' in combined_df.columns:
        combined_df['Euro_Gold_Index'] = combined_df['Gold_Close'] / combined_df['Euro_Close']

    return combined_df

market_data = fetch_market_data()

def rename_columns(df):
    rename_map = {
        "GC=F": "Gold",
        "^GSPC": "SP500",
        "^DJI": "DowJones",
        "EUR=X": "Euro",
        "^STOXX50E": "EuroStoxx",
        "CL=F": "CrudeOil",
        "AAPL": "Apple",
        "^TNX": "USBonds10Y",
        "KBE": "USBankETF",
        "PL=F": "Platinum",
        "PA=F": "Palladium",
        "GDX": "GoldMinersETF",
        "USO": "USOilETF",
        "DX-Y.NYB": "USDIndex"
    }

    new_columns = []
    for col in df.columns:
        for raw, clean in rename_map.items():
            if raw in col:
                col = col.replace(raw, clean)
        if '_' in col:
            parts = col.split('_')
            if parts[0] in ['Open', 'High', 'Low', 'Close', 'Adj', 'Volume', 'AdjClose']:
                col = f"{parts[1]}_{parts[0]}"
        new_columns.append(col)
    df.columns = new_columns
    return df

df = rename_columns(market_data)

# ------------------ FRED DATA FETCHING ------------------
def fetch_fred_data():
    cpi = fred.get_series('CPIAUCSL')
    irate = fred.get_series('FEDFUNDS')
    cpi = cpi.resample('D').ffill().to_frame(name='CPI')
    irate = irate.resample('D').ffill().to_frame(name='Interest_Rate')
    return cpi, irate

# ------------------ DATA PREPARATION  ------------------
def prepare_data():
    market = market_data
    cpi, irate = fetch_fred_data()
    df = market.join([cpi, irate], how='inner')
    df['Prev_Gold_Close'] = df['Gold_Close'].shift(1)
    df['Prev_Gold_High'] = df['Gold_High'].shift(1)
    df = df.dropna()
    return df

# ------------------ MODEL TRAINING ------------------
def train_model(df, model_type="Linear Regression", target="Close"):
    features = [
        'Prev_Gold_Close',
        'Prev_Gold_High',
        'SP500_Close',
        'DowJones_Close',
        'Euro_Close',
        'EuroStoxx_Close',
        'CrudeOil_Close',
        'Apple_Close',
        'USBonds10Y_Close',
        'USBankETF_Close',
        'Platinum_Close',
        'Palladium_Close',
        'GoldMinersETF_Close',
        'USOilETF_Close',
        'USDIndex_Close',
        'CPI',
        'Interest_Rate'
    ]
    X = df[features]
    y = df[f"Gold_{target}"]

    if model_type == "Linear Regression":
        model = LinearRegression()
    elif model_type == "Random Forest":
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    elif model_type == "SVR":
        model = SVR()
    else:
        raise ValueError("Unsupported model type selected")

    model.fit(X, y)
    joblib.dump(model, f"model_{model_type.replace(' ', '_')}_{target}.pkl")
    return model

# ------------------ MODEL LOADING OR TRAINING ------------------
def load_or_train_model(df, model_type="Linear Regression", target="Close"):
    model_path = os.path.join(MODEL_DIR, f"model_{model_type.replace(' ', '_')}_{target}.pkl")
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        return train_model(df, model_type, target)

# ------------------ GET LATEST INPUTS ------------------
def get_latest_inputs():
    today = datetime.datetime.today()
    past = today - datetime.timedelta(days=10)

    # Fetch all relevant tickers
    gold = yf.download("GC=F", start=past, end=today)[['Close', 'High']].rename(
        columns={'Close': 'Gold_Close', 'High': 'Gold_High'}
    )
    tickers = {
        'SP500_Close': "^GSPC",
        'DowJones_Close': "^DJI",
        'Euro_Close': "EUR=X",
        'EuroStoxx_Close': "^STOXX50E",
        'CrudeOil_Close': "CL=F",
        'Apple_Close': "AAPL",
        'USBonds10Y_Close': "^TNX",
        'USBankETF_Close': "KBE",
        'Platinum_Close': "PL=F",
        'Palladium_Close': "PA=F",
        'GoldMinersETF_Close': "GDX",
        'USOilETF_Close': "USO",
        'USDIndex_Close': "DX-Y.NYB"
    }

    # Download all tickers into one dataframe
    all_data = [gold]
    for colname, ticker in tickers.items():
        temp = yf.download(ticker, start=past, end=today)[['Close']]
        if temp.empty:
            raise ValueError(f"❌ No data fetched for {ticker}")
        temp = temp.rename(columns={'Close': colname})
        all_data.append(temp)  # ✅ Fix: append temp to all_data

    df = pd.concat(all_data, axis=1).dropna()
    
    if df.empty:
        raise ValueError("❌ Combined dataframe is empty. Could not fetch market indicators.")

    latest = df.iloc[-1]
    latest_date = df.index[-1]

    # Get latest FRED values
    cpi = float(fred.get_series('CPIAUCSL').iloc[-1])
    irate = float(fred.get_series('FEDFUNDS').iloc[-1])

    # Feature dict to match training features
    features = {
        'Prev_Gold_Close': float(latest['Gold_Close']),
        'Prev_Gold_High': float(latest['Gold_High']),
        'SP500_Close': float(latest['SP500_Close']),
        'DowJones_Close': float(latest['DowJones_Close']),
        'Euro_Close': float(latest['Euro_Close']),
        'EuroStoxx_Close': float(latest['EuroStoxx_Close']),
        'CrudeOil_Close': float(latest['CrudeOil_Close']),
        'Apple_Close': float(latest['Apple_Close']),
        'USBonds10Y_Close': float(latest['USBonds10Y_Close']),
        'USBankETF_Close': float(latest['USBankETF_Close']),
        'Platinum_Close': float(latest['Platinum_Close']),
        'Palladium_Close': float(latest['Palladium_Close']),
        'GoldMinersETF_Close': float(latest['GoldMinersETF_Close']),
        'USOilETF_Close': float(latest['USOilETF_Close']),
        'USDIndex_Close': float(latest['USDIndex_Close']),
        'CPI': cpi,
        'Interest_Rate': irate
    }

    return features, float(latest['Gold_Close']), float(latest['Gold_High']), latest_date


# ------------------ PREDICTION FUNCTION ------------------
def predict_next_price(features, model):
    X = np.array(list(features.values())).reshape(1, -1)
    return model.predict(X)[0]

# ------------------ PEAK AND TROUGH FUNCTION ------------------
def get_peak_and_trough(pred_date, window=30):
    start = pred_date - datetime.timedelta(days=window)
    end = pred_date

    gold = yf.download("GC=F", start=start, end=end)[['Close']].rename(columns={'Close': 'Gold_Close'}).dropna()

    if gold.empty:
        return None, None, None, None, pd.DataFrame()

    peak_value = float(gold['Gold_Close'].max())
    trough_value = float(gold['Gold_Close'].min())

    peak_date = gold['Gold_Close'].idxmax()
    trough_date = gold['Gold_Close'].idxmin()

    if isinstance(peak_date, pd.Series):
        peak_date = peak_date.iloc[0]
    if isinstance(trough_date, pd.Series):
        trough_date = trough_date.iloc[0]

    return peak_value, trough_value, peak_date.strftime('%Y-%m-%d'), trough_date.strftime('%Y-%m-%d'), gold


# ------------------ MODEL COMPARISON ------------------
def compare_models(df, target="Close"):
    features = [
        'Prev_Gold_Close', 'Prev_Gold_High', 'SP500_Close', 'DowJones_Close',
        'Euro_Close', 'EuroStoxx_Close', 'CrudeOil_Close', 'Apple_Close',
        'USBonds10Y_Close', 'USBankETF_Close', 'Platinum_Close', 'Palladium_Close',
        'GoldMinersETF_Close', 'USOilETF_Close', 'USDIndex_Close', 'CPI', 'Interest_Rate'
    ]
    X = df[features]
    y = df[f"Gold_{target}"]
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "SVR": SVR()
    }
    
    scores = {}
    
    for name, model in models.items():
        model.fit(X, y)
        pred = model.predict(X)
        r2 = r2_score(y, pred)
        scores[name] = r2
        print(f"{name} R2 Score: {r2:.4f}")
    
    best_model_type = max(scores, key=scores.get)
    
    print(f"\n✅ Best Model: {best_model_type} with R² = {scores[best_model_type]:.4f}")
    
    return best_model_type, scores
