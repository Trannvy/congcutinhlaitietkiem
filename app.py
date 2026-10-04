import streamlit as st
st.image("funny cat meme.jpg")

# Cấu hình trang
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm - Trần Ngọc Thúy Vy",
    page_icon="💰",
    layout="centered"
)

# Tiêu đề chính của ứng dụng
st.title("ỨNG DỤNG TÍNH LÃI GỬI TIẾT KIỆM_TRẦN NGỌC THÚY VY")

# Tạo 2 Tab chức năng
tab_normal, tab_zombie = st.tabs(["📊 Tính Lãi Tiết Kiệm", "🧟 Chế Độ Tận Thế & Siêu Lạm Phát"])

# ===================================================================
# TAB 1: TÍNH LÃI TIẾT KIỆM CHUẨN (CODE GỐC CỦA BẠN)
# ===================================================================
with tab_normal:
    st.write("Nhập thông tin tiền gửi bên dưới để tính toán lãi tiết kiệm theo **lãi đơn** hoặc **lãi kép**.")
    st.divider()

    # Layout nhập liệu 2 cột
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

    # Nút tính toán
    if st.button("🚀 Tính Tiền Lãi", type="primary", use_container_width=True, key="btn_normal"):
        r_thang = (lai_suat_nam / 100) / 12  # Lãi suất theo tháng
        
        # Xác định chu kỳ lãnh lãi (số tháng)
        if hinh_thuc_lanh == "Lãnh lãi theo tháng":
            m = 1
        elif hinh_thuc_lanh == "Lãnh lãi theo quý":
            m = 3
        else:  # Lãnh lãi cuối kỳ
            m = ky_han_thang

        # Kiểm tra tính hợp lệ của kỳ hạn với hình thức lãnh lãi
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

        # Hiển thị số liệu dạng thẻ Metric
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.metric(
                label=f"Tài sản cuối kỳ ({ky_han_thang} tháng)", 
                value=f"{tong_tien:,.0f} VNĐ".replace(",", ".")
            )
            st.metric(
                label="Tổng tiền lãi nhận được", 
                value=f"{tong_lai:,.0f} VNĐ".replace(",", ".")
            )

        with res_col2:
            st.metric(
                label="Tiền gốc ban đầu", 
                value=f"{so_tien_gui:,.0f} VNĐ".replace(",", ".")
            )
            label_dinh_ky = "Tiền lãi nhận mỗi kỳ" if loai_lai == "Lãi đơn" else "Lãi nhận trung bình/kỳ"
            st.metric(
                label=f"{label_dinh_ky} ({m} tháng/kỳ)", 
                value=f"{lai_dinh_ky:,.0f} VNĐ".replace(",", ".")
            )

        # Hiển thị bảng chi tiết các kỳ nhận lãi
        with st.expander("📝 Xem bảng chi tiết nhận lãi qua từng kỳ"):
            lich_trinh = []
            goc_dau_ky = so_tien_gui
            
            for i in range(1, so_chu_ky + 1):
                if loai_lai == "Lãi đơn":
                    lai_ky = lai_dinh_ky
                    goc_cuoi_ky = so_tien_gui
                else:
                    lai_ky = goc_dau_ky * r_chu_ky
                    goc_cuoi_ky = goc_dau_ky + lai_ky
                    
                lich_trinh.append({
                    "Kỳ": f"Kỳ {i} (Tháng {i * m})",
                    "Tiền gốc đầu kỳ (VNĐ)": f"{goc_dau_ky:,.0f}".replace(",", "."),
                    "Lãi nhận được (VNĐ)": f"{lai_ky:,.0f}".replace(",", "."),
                    "Tổng tích lũy (VNĐ)": f"{(goc_cuoi_ky if loai_lai == 'Lãi kép' else so_tien_gui + lai_ky * i):,.0f}".replace(",", ".")
                })
                goc_dau_ky = goc_cuoi_ky

            st.dataframe(lich_trinh, use_container_width=True)


# ===================================================================
# TAB 2: CHẾ ĐỘ TẬN THẾ & SIÊU LẠM PHÁT (TÍNH NĂNG MỚI)
# ===================================================================
with tab_zombie:
    st.error("⚠️ CẢNH BÁO: GIẢ LẬP KHỦNG HOẢNG TÀI CHÍNH VÀ SIÊU LẠM PHÁT!")
    st.write("Kiểm tra sức mua thực tế của khoản tiết kiệm khi nền kinh tế bị **'Zombie Lạm Phát'** tấn công.")

    st.subheader("1. Cấu hình kịch bản Tận Thế")
    z_col1, z_col2 = st.columns(2)
    
    with z_col1:
        z_tien_gui = st.number_input(
            "Số tiền gửi (VNĐ):", 
            min_value=1_000_000, 
            value=100_000_000, 
            step=10_000_000,
            format="%d",
            key="z_tien_gui"
        )
        z_nam = st.slider("Số năm gửi tiết kiệm trong tận thế:", min_value=1, max_value=10, value=3)

    with z_col2:
        z_lai_suat = st.number_input(
            "Lãi suất ngân hàng (%/năm):", 
            min_value=0.0, 
            value=6.0, 
            step=0.5,
            key="z_lai_suat"
        )
        z_mon_an = st.selectbox("Chọn đơn vị đo lường sức mua:", ["Bát Phở (50.000 VNĐ)", "Ổ Bánh Mì (20.000 VNĐ)"])

    st.subheader("2. Mức độ Siêu Lạm Phát (Kéo thanh trượt để giả lập)")
    lam_phat = st.slider(
        "Tỷ lệ lạm phát hàng năm (%):", 
        min_value=3, 
        max_value=200, 
        value=30, 
        step=5,
        help="Lạm phát thông thường ~3-5%. Khủng hoảng: 20-50%. Siêu lạm phát: >100%"
    )

    # Đơn giá ban đầu
    gia_ban_dau = 50000 if "Phở" in z_mon_an else 20000
    ten_mon = "Bát phở" if "Phở" in z_mon_an else "Ổ bánh mì"

    if st.button("🚨 KÍCH HOẠT MÔ PHỎNG TẬN THẾ", type="primary", use_container_width=True, key="btn_zombie"):
        # Tính tổng tiền gửi theo lãi kép
        tong_tien_nhan = z_tien_gui * ((1 + z_lai_suat / 100) ** z_nam)
        
        # Giá món ăn sau N năm siêu lạm phát
        gia_mon_tuong_lai = gia_ban_dau * ((1 + lam_phat / 100) ** z_nam)
        
        # Sức mua (Số lượng món ăn)
        so_mon_hien_tai = z_tien_gui / gia_ban_dau
        so_mon_tuong_lai = tong_tien_nhan / gia_mon_tuong_lai
        phantram_bien_dong = ((so_mon_tuong_lai - so_mon_hien_tai) / so_mon_hien_tai) * 100

        st.divider()
        st.subheader("💀 KẾT QUẢ SỨC MUA THỰC TẾ")

        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(
                label="Hôm nay mua được", 
                value=f"{so_mon_hien_tai:,.0f} {ten_mon}".replace(",", ".")
            )
        with m_col2:
            st.metric(
                label=f"Sau {z_nam} năm mua được", 
                value=f"{so_mon_tuong_lai:,.0f} {ten_mon}".replace(",", "."),
                delta=f"{phantram_bien_dong:.1f}% sức mua",
                delta_color="normal"
            )
        with m_col3:
            st.metric(
                label=f"Giá 1 {ten_mon} lúc đó", 
                value=f"{gia_mon_tuong_lai:,.0f} VNĐ".replace(",", ".")
            )

        # Đánh giá cấp độ nguy hiểm
        st.subheader("🩺 Đánh Giá Mức Độ Nguy Hiểm")
        if lam_phat <= 8:
            st.success("🟢 **An toàn:** Lạm phát ở mức kiểm soát. Tiết kiệm ngân hàng vẫn bảo toàn hoặc gia tăng giá trị thực.")
        elif lam_phat <= 20:
            st.warning("🟡 **Cảnh báo Lạm Phát Cao:** Tiền lãi ngân hàng bị bào mòn. Sức mua giảm nhẹ qua từng năm.")
        elif lam_phat <= 50:
            st.error("🟠 **Nguy hiểm (Bão Lạm Phát):** Đồng tiền mất giá nhanh chóng! Tiền lãi không bù đắp nổi đà tăng giá hàng hóa.")
        else:
            st.error("💀 **TẬN THẾ TÀI CHÍNH (Siêu Lạm Phát):** Tiền giấy biến thành 'giấy vụn'. Giữ tiền tiết kiệm đồng nghĩa với việc mất trắng tài sản!")

        # Gợi ý hành động trú ẩn
        with st.expander("🛡️ GỢI Ý HÀNH ĐỘNG TRÚ ẨN TÀI CHÍNH"):
            if lam_phat > 20:
                st.markdown("""
                * **🥇 Vàng vật chất:** Kênh trú ẩn lịch sử chống lại sự sụp đổ của tiền giấy.
                * **🌾 Hàng hóa thiết yếu & Lương thực:** Tích trữ tài sản có giá trị sử dụng trực tiếp.
                * **💵 Ngoại tệ mạnh:** Chuyển đổi một phần sang các đồng tiền có độ ổn định cao hơn.
                * **🏠 Bất động sản / Tài sản thực:** Giữ tài sản không thể tự dưng in thêm.
                * **🚫 HÀNH ĐỘNG CẦN TRÁNH:** Không rút tiền mặt để dưới gối, không gia hạn các hợp đồng tiết kiệm dài hạn cố định lãi suất thấp.
                """)
            else:
                st.markdown("""
                * **🏦 Tiếp tục gửi tiết kiệm:** Lãi suất thực dương giúp tài sản an toàn.
                * **📊 Đa dạng hóa:** Có thể trích 20-30% sang các kênh tăng trưởng khác như chứng khoán hoặc quỹ mở.
                """)
