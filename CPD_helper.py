import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

# preprocess data
def preprocess_data(file_path):
    file_name = file_path
    df = pd.read_excel(file_name)

    df['Date'] = pd.to_datetime(df['Date'])
    # Convert timestamps to Unix timestamps (seconds since epoch)
    df['UnixTs'] = df['Date'].astype('int64') // 10**9  # Convert nanoseconds to seconds


    # create portofolio value & return 
    df['Portfolio_Value'] = df['AU_PX_LAST'] * 500 + df['AG_PX_LAST'] * 100000 + df['PT_PX_LAST'] * 5000 + df['PD_PX_LAST'] * 2000
    df['Portfolio_Return'] = np.log(df['Portfolio_Value'] / df['Portfolio_Value'].shift(-1))

    # add volatility attributes
    window_size = 5

    day_volatility = pd.Series(df['Portfolio_Return']).rolling(window=window_size).std().dropna() * 100
    df = df.drop(df.index[:window_size])

    # scale by 10o times
    # Define thresholds for low, medium, and high volatility regimes
    low_threshold = np.percentile(day_volatility, 33)
    high_threshold = np.percentile(day_volatility, 66)

    # Classify volatility into regimes based on thresholds
    regime_labels = np.where(day_volatility < low_threshold, 'L',
                            np.where(day_volatility < high_threshold, 'M', 'H'))

    # Create a DataFrame with volatility data and regime labels
    df[['Volatility', 'Regime']] = pd.DataFrame({'Volatility': day_volatility, 'Regime': regime_labels})

    return df

def classify_volatility(volatility, low_threshold, medium_threshold):
    return 'High' if volatility >= medium_threshold else \
           'Medium' if volatility >= low_threshold else 'Low'

def predict_volatility(val_data):
    # predict today's regime
    last_record = val_data[-1]
    reshaped_data = np.expand_dims(last_record, axis=0).reshape((1,) + last_record.shape)
    x = cpd_model.predict(reshaped_data)

    pred_volatility = x[0][4][0]

    classify_volatility(pred_volatility, low_threshold, high_threshold)
    print(f"The volatility level is: {result}")

    return pred_volatility

