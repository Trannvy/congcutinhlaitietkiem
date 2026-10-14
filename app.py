import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
import tensorflow as tf
import yfinance as yf

# --- CỐ ĐỊNH SEED CHO MÔ HÌNH ---
seed = 42
np.random.seed(seed)
tf.random.set_seed(seed)
random.seed(seed)

# --- GIAO DIỆN STREAMLIT ---
st.title("📈 Ứng Dụng Dự Đoán Giá Cổ Phiếu bằng LSTM")
st.write("Ứng dụng sử dụng mô hình học sâu LSTM theo chuẩn bài học của giảng viên.")

# Sidebar (Thanh công cụ bên trái) để cấu hình
st.sidebar.header("Cấu hình tham số")
ticker = st.sidebar.text_input("Nhập mã cổ phiếu (VD: VNM.VN, VIC, AAPL):", "VNM.VN")
start_date = st.sidebar.date_input("Ngày bắt đầu", value=pd.to_datetime("2018-01-01"))
end_date = st.sidebar.date_input("Ngày kết thúc", value=pd.to_datetime("2026-10-14"))

epochs = st.sidebar.slider("Số Epochs huấn luyện:", 5, 30, 10)
future_days = st.sidebar.slider("Số ngày dự đoán tương lai:", 5, 30, 10)

if st.button("Bắt đầu huấn luyện và dự đoán"):
  with st.spinner("Đang tải dữ liệu và huấn luyện mô hình LSTM... Vui lòng đợi trong giây lát!"):
    
    # 1. Tải dữ liệu
    df = yf.download(ticker, start=start_date, end=end_date)
    if df.empty:
      st.error("Không tìm thấy dữ liệu cho mã này. Vui lòng kiểm tra lại mã cổ phiếu!")
    else:
      # Xử lý đa cấp index của yfinance nếu có
      if isinstance(df.columns, pd.MultiIndex):
        close_data = df[("Close", ticker)].values
      else:
        close_data = df["Close"].values

      data = close_data.reshape(-1, 1)

      # 2. Chia tập dữ liệu
      train_size = int(0.8 * len(data))
      train_data = data[:train_size]
      test_data = data[train_size:]

      # 3. Chuẩn hóa dữ liệu
      scaler = MinMaxScaler()
      train_scaled = scaler.fit_transform(train_data)
      test_scaled = scaler.transform(test_data)

      # Hàm tạo chuỗi
      def create_sequences(seq_data, window_size=60):
        X, y = [], []
        for i in range(window_size, len(seq_data)):
          X.append(seq_data[i - window_size : i])
          y.append(seq_data[i])
        return np.array(X), np.array(y)

      X_train, y_train = create_sequences(train_scaled)
      test_combined = np.vstack((train_scaled[-60:], test_scaled))
      X_test, y_test = create_sequences(test_combined)

      X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
      X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

      val_size = int(0.1 * len(X_train))
      X_val = X_train[-val_size:]
      y_val = y_train[-val_size:]
      X_train_final = X_train[:-val_size]
      y_train_final = y_train[:-val_size]

      # 4. Xây dựng mô hình LSTM
      from tensorflow.keras.callbacks import EarlyStopping
      from tensorflow.keras.layers import LSTM, Dense
      from tensorflow.keras.models import Sequential

      model = Sequential()
      model.add(LSTM(50, return_sequences=True, input_shape=(60, 1)))
      model.add(LSTM(50))
      model.add(Dense(1))
      model.compile(optimizer="adam", loss="mean_squared_error")

      early_stop = EarlyStopping(
          monitor="val_loss", patience=5, restore_best_weights=True
      )

      history = model.fit(
          X_train_final,
          y_train_final,
          validation_data=(X_val, y_val),
          epochs=epochs,
          batch_size=32,
          shuffle=False,
          callbacks=[early_stop],
          verbose=0,
      )

      # 5. Dự báo trên tập Test
      test_pred = model.predict(X_test)
      test_pred = scaler.inverse_transform(test_pred)
      y_test_real = scaler.inverse_transform(y_test.reshape(-1, 1))

      # Tính toán đánh giá
      rmse = np.sqrt(mean_squared_error(y_test_real, test_pred))
      mae = mean_absolute_error(y_test_real, test_pred)
      r2 = r2_score(y_test_real, test_pred)

      # Hiển thị thông số đánh giá lên web
      st.subheader("📊 Đánh giá hiệu suất mô hình trên tập Test")
      col1, col2, col3 = st.columns(3)
      col1.metric("RMSE", f"{rmse:.2f}")
      col2.metric("MAE", f"{mae:.2f}")
      col3.metric("R2 Score", f"{r2:.2f}")

      # Biểu đồ Loss
      st.subheader("📉 Biểu đồ Loss (Train vs Validation)")
      fig_loss, ax_loss = plt.subplots(figsize=(10, 4))
      ax_loss.plot(history.history["loss"], label="Train Loss")
      ax_loss.plot(history.history["val_loss"], label="Validation Loss")
      ax_loss.legend()
      st.pyplot(fig_loss)

      # Biểu đồ so sánh giá thật và dự báo Test
      st.subheader("📉 Biểu đồ so sánh Giá Thật và Dự Báo")
      fig_test, ax_test = plt.subplots(figsize=(12, 5))
      ax_test.plot(y_test_real, label="Giá thật", color="orange")
      ax_test.plot(test_pred, label="Dự báo test", color="blue")
      ax_test.legend()
      st.pyplot(fig_test)

      # 6. Dự báo tương lai tiếp theo
      last_60_days = np.vstack((train_scaled, test_scaled))[-60:]
      last_60_days = last_60_days.reshape(1, 60, 1)
      future_predictions = []

      for i in range(future_days):
        next_pred = model.predict(last_60_days)
        future_predictions.append(next_pred[0, 0])
        last_60_days = np.append(
            last_60_days[:, 1:, :], next_pred.reshape(1, 1, 1), axis=1
        )

      future_predictions = np.array(future_predictions).reshape(-1, 1)
      future_predictions = scaler.inverse_transform(future_predictions)

      st.subheader(f"🔮 Kết quả dự báo {future_days} ngày tới")
      df_future = pd.DataFrame(future_predictions, columns=["Giá dự báo tương lai"])
      st.dataframe(df_future)

      # Biểu đồ tổng hợp bao gồm cả tương lai
      st.subheader("📈 Biểu đồ xu hướng và dự báo tương lai")
      fig_future, ax_future = plt.subplots(figsize=(12, 6))
      ax_future.plot(y_test_real, label="Giá thật", color="orange")
      ax_future.plot(test_pred, label="Dự báo test", color="blue")
      future_x = range(len(y_test_real), len(y_test_real) + len(future_predictions))
      ax_future.plot(future_x, future_predictions, marker="o", label="Tương lai", color="green")
      ax_future.legend()
      st.pyplot(fig_future)
