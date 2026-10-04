import streamlit as st
st.image("funny cat meme.jpg")

# Cấu hình trang (Bắt buộc đặt lệnh Streamlit ngay sau)
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm - Trần Ngọc Thúy Vy",
    page_icon="💰",
    layout="centered"
)

# Tiêu đề chính
st.title("ỨNG DỤNG TÍNH LÃI GỬI TIẾT KIỆM_TRẦN NGỌC THÚY VY")

# Tạo 2 Tab chức năng
tab_normal, tab_creative = st.tabs(["📊 Tính Lãi Tiết Kiệm", "🧋 Quy Đổi Lãi & Rút Sớm"])

# ===================================================================
# TAB 1: TÍNH LÃI CHUẨN (CODE GỐC CỦA BẠN)
# ===================================================================
with tab_normal:
    st.write("Nhập thông tin tiền gửi bên dưới để tính toán lãi tiết kiệm theo **lãi đơn** hoặc **lãi kép**.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        so_tien_gui = st.number_input(
            "Số tiền gửi (VNĐ):", 
            min_value=1_000_000, 
            value=100_000_000, 
            step=5_000_000,
            format="%d",
            key="normal_tien_gui"
        )
        ky_han_thang = st.number_input(
            "Kỳ hạn gửi (Tháng):", 
            min_value=1, 
            value=12, 
            step=1,
            key="normal_ky_han"
        )

    with col2:
        lai_suat_nam = st.number_input(
            "Lãi suất (%/năm):", 
            min_value=0.1, 
            max_value=20.0, 
            value=6.0, 
            step=0.1,
            format="%.1f",
            key="normal_lai_suat"
        )
        loai_lai = st.selectbox(
            "Phương thức tính lãi:",
            options=["Lãi đơn", "Lãi kép"],
            key="normal_loai_lai"
        )

    hinh_thuc_lanh = st.selectbox(
        "Hình thức lãnh lãi:",
        options=["Lãnh lãi theo tháng", "Lãnh lãi theo quý", "Lãnh lãi cuối kỳ"],
        key="normal_lanh_lai"
    )

    if st.button("🚀 Tính Tiền Lãi", type="primary", use_container_width=True, key="btn_normal"):
        r_thang = (lai_suat_nam / 100) / 12
        m = 1 if hinh_thuc_lanh == "Lãnh lãi theo tháng" else (3 if hinh_thuc_lanh == "Lãnh lãi theo quý" else ky_han_thang)

        if ky_han_thang % m != 0 and hinh_thuc_lanh != "Lãnh lãi cuối kỳ":
            st.warning(f"⚠️ Kỳ hạn gửi ({ky_han_thang} tháng) không chia hết cho chu kỳ {hinh_thuc_lanh.lower()}. Kết quả tính theo số chu kỳ chẵn.")

        so_chu_ky = ky_han_thang // m
        
        if loai_lai == "Lãi đơn":
            lai_dinh_ky = so_tien_gui * r_thang * m
            tong_lai = lai_dinh_ky * so_chu_ky
            tong_tien = so_tien_gui + tong_lai
        else:
            r_chu_ky = r_thang * m
            tong_tien = so_tien_gui * ((1 + r_chu_ky) ** so_chu_ky)
            tong_lai = tong_tien - so_tien_gui
            lai_dinh_ky = tong_lai / so_chu_ky if so_chu_ky > 0 else 0

        st.divider()
        st.subheader("📊 Kết Quả Tính Toán")

        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("Tài sản cuối kỳ", f"{tong_tien:,.0f} VNĐ".replace(",", "."))
            st.metric("Tổng tiền lãi nhận được", f"{tong_lai:,.0f} VNĐ".replace(",", "."))
        with res_col2:
            st.metric("Tiền gốc ban đầu", f"{so_tien_gui:,.0f} VNĐ".replace(",", "."))
            label_dinh_ky = "Tiền lãi nhận mỗi kỳ" if loai_lai == "Lãi đơn" else "Lãi nhận trung bình/kỳ"
            st.metric(f"{label_dinh_ky} ({m} tháng)", f"{lai_dinh_ky:,.0f} VNĐ".replace(",", "."))

        with st.expander("📝 Xem bảng chi tiết nhận lãi qua từng kỳ"):
            lich_trinh = []
            goc_dau_ky = so_tien_gui
            for i in range(1, so_chu_ky + 1):
                lai_ky = lai_dinh_ky if loai_lai == "Lãi đơn" else goc_dau_ky * r_chu_ky
                goc_cuoi_ky = so_tien_gui if loai_lai == "Lãi đơn" else goc_dau_ky + lai_ky
                lich_trinh.append({
                    "Kỳ": f"Kỳ {i} (Tháng {i * m})",
                    "Tiền gốc đầu kỳ (VNĐ)": f"{goc_dau_ky:,.0f}".replace(",", "."),
                    "Lãi nhận được (VNĐ)": f"{lai_ky:,.0f}".replace(",", "."),
                    "Tổng tích lũy (VNĐ)": f"{(goc_cuoi_ky if loai_lai == 'Lãi kép' else so_tien_gui + lai_ky * i):,.0f}".replace(",", ".")
                })
                goc_dau_ky = goc_cuoi_ky
            st.dataframe(lich_trinh, use_container_width=True)

# ===================================================================
# TAB 2: QUY ĐỔI LÃI VUI & CẢNH BÁO RÚT SỚM (Ý TƯỞNG MỚI ĐƠN GIẢN)
# ===================================================================
with tab_creative:
    st.subheader("🧋 1. Tiền Lãi Của Bạn Mua Được Bằng Nào Món?")
    c_tien_gui = st.number_input("Số tiền gửi (VNĐ):", value=50_000_000, step=5_000_000, key="c_tien")
    c_lai_suat = st.number_input("Lãi suất (%/năm):", value=6.0, step=0.5, key="c_lai")
    c_thang = st.number_input("Số tháng gửi:", value=12, min_value=1, key="c_thang")

    tien_lai_du_kien = c_tien_gui * (c_lai_suat / 100 / 12) * c_thang

    st.write(f"👉 Với **{tien_lai_du_kien:,.0f} VNĐ** tiền lãi, bạn có thể tự thưởng cho mình:".replace(",", "."))
    
    q_col1, q_col2, q_col3 = st.columns(3)
    with q_col1:
        st.metric("🧋 Ly Trà Sữa", f"{int(tien_lai_du_kien // 50000)} ly", "50k / ly")
    with q_col2:
        st.metric("🎬 Vé Xem Phim", f"{int(tien_lai_du_kien // 110000)} vé", "110k / vé")
    with q_col3:
        st.metric("✈️ Vé Máy Bay Nội Địa", f"{int(tien_lai_du_kien // 1500000)} vé", "1.5tr / vé")

    st.divider()

    st.subheader("🚨 2. Cảnh Báo Phạt Rút Tiền Trước Hạn")
    st.caption("Nếu rút trước hạn, ngân hàng thường chuyển về lãi suất Không kỳ hạn (~0.2%/năm).")
    
    thang_rut_som = st.slider("Giả sử bạn phải rút gấp ở tháng thứ:", min_value=1, max_value=int(c_thang), value=int(c_thang // 2))

    # Tính lãi thực nhận khi rút sớm (lãi không kỳ hạn 0.2%)
    lai_khong_ky_han = c_tien_gui * (0.2 / 100 / 12) * thang_rut_som
    lai_dung_ky = c_tien_gui * (c_lai_suat / 100 / 12) * thang_rut_som
    tien_mat = lai_dung_ky - lai_khong_ky_han

    st.error(f"💸 Nếu rút ở tháng thứ {thang_rut_som}, bạn chỉ nhận **{lai_khong_ky_han:,.0f} VNĐ** tiền lãi.")
    st.warning(f"📉 Số tiền lãi bị mất đi (tiếc nuối): **{tien_mat:,.0f} VNĐ**!".replace(",", "."))
