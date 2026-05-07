import streamlit as st
import time
import pandas as pd
import plotly.express as px
from protocol.stop_and_wait import run_stop_and_wait
from protocol.sliding_window import run_sliding_window

# Səhifə tənzimləmələri
st.set_page_config(page_title="UDP Reliable Transfer Pro", layout="wide")

# Müəllim və Tələbə məlumatı
st.title("🌐 Reliable Data Transfer over UDP")
st.markdown("---")
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.info("**Tələbə:** Punhan Mursaliyev")
with col_info2:
    st.success("**Müəllim:** Nağızadə Elşən")

# SIDEBAR - Parametrlər
st.sidebar.header("🛠 Şəbəkə Parametrləri")
method = st.sidebar.selectbox("Protokol Metodu", ["Stop-and-Wait", "Sliding Window"])
loss_rate = st.sidebar.slider("Paket İtki Faizi (%)", 0, 50, 5)
latency = st.sidebar.slider("Gecikmə (ms)", 0, 1000, 100)

w_size = 1
if method == "Sliding Window":
    w_size = st.sidebar.number_input("Pəncərə Ölçüsü (Window Size)", 1, 10, 4)

# Əsas ekran sütunları
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Canlı Performans Monitoru")
    prog_bar = st.progress(0)
    status_text = st.empty()
    chart_placeholder = st.empty()

with col2:
    st.subheader("📜 Hadisə Logları")
    log_area = st.empty()

# Prosesi başlatmaq
if st.button("🚀 Transferi Başlat"):
    # Simulyasiya üçün 50 paketi əvəz edən data
    fake_file_data = b"X" * 51200 # Təxminən 50 paket (hərəsi 1024 byte)
    start_time = time.time()
    
    logs = []
    plot_data = []
    
    # UI Yeniləmə funksiyası (Protokol faylları tərəfindən çağırılır)
    def update_dashboard(current, total, msg, is_error):
        perc = int((current / total) * 100)
        prog_bar.progress(perc)
        
        # Logları yenilə
        icon = "🔴" if is_error else "🟢"
        logs.insert(0, f"{icon} {msg}")
        log_area.text("\n".join(logs[:15]))
        
        # Qrafik üçün data yığ
        elapsed = time.time() - start_time
        throughput = (current * 1024) / (elapsed + 0.1) / 1024 # KB/s
        plot_data.append({"Zaman": round(elapsed, 1), "Sürət (KB/s)": round(throughput, 2)})
        
        df = pd.DataFrame(plot_data)
        fig = px.line(df, x="Zaman", y="Sürət (KB/s)", title="Anlıq Ötürmə Sürəti")
        chart_placeholder.plotly_chart(fig, use_container_width=True)

    # Seçilən metodu icra et
    if method == "Stop-and-Wait":
        retrans = run_stop_and_wait(fake_file_data, loss_rate, latency, update_dashboard)
    else:
        retrans = run_sliding_window(fake_file_data, loss_rate, latency, w_size, update_dashboard)
    
    end_time = time.time()
    total_duration = round(end_time - start_time, 2)
    
    # Nəticə Hesabatı
    st.markdown("---")
    res1, res2, res3 = st.columns(3)
    res1.metric("Ümumi Vaxt", f"{total_duration} san")
    res2.metric("Təkrar Göndərmə", f"{retrans} paket")
    res3.metric("Status", "Uğurlu ✅")
    st.balloons()