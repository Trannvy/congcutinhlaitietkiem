import streamlit as st
st.image("funny cat meme.jpg")

# Cấu hình trang (Lệnh Streamlit bắt buộc đặt ở đầu)
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm - Trần Ngọc Thúy Vy",
    page_icon="💰",
    layout="centered"
)

# Tiêu đề chính của ứng dụng
st.title("ỨNG DỤNG TÍNH LÃI GỬI TIẾT KIỆM_TRẦN NGỌC THÚY VY")

# Tạo 3 Tab chức năng
tab_normal, tab_creative, tab_inflation = st.tabs([
    "📊 Tính Lãi Tiết Kiệm", 
    "🎯 Mục Tiêu & Giả Lập Rút Sớm", 
    "🎈 Tác Động Lạm Phát"
])

# ===================================================================
# TAB 1: TÍNH LÃI TIẾT KIỆM CHUẨN (CODE GỐC CỦA BẠN)
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
        r_thang = (lai_suat_nam / 100) / 12  # Lãi suất theo tháng
        
        m = 1 if hinh_thuc_lanh == "Lãnh lãi theo tháng" else (3 if hinh_thuc_lanh == "Lãnh lãi theo quý" else ky_han_thang)

        if ky_han_thang % m != 0 and hinh_thuc_lanh != "Lãnh lãi cuối kỳ":
            st.warning(f"⚠️️ Kỳ hạn gửi ({ky_han_thang} tháng) không chia hết cho chu kỳ {hinh_thuc_lanh.lower()}. Kết quả tính theo số chu kỳ chẵn.")

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
# TAB 2: LÃI KÉP NGƯỢC & GIẢ LẬP RÚT TIỀN TRƯỚC HẠN
# ===================================================================
with tab_creative:
    st.subheader("🎯 1. Tính Toán Tiền Gửi Cho Mục Tiêu Tài Chính")
    st.caption("Nhập số tiền bạn muốn đạt được trong tương lai để tính tiền gửi ban đầu hoặc tiền gửi góp hàng tháng.")

    col_rev1, col_rev2 = st.columns(2)
    with col_rev1:
        muc_tieu = st.number_input(
            "Số tiền mục tiêu (VNĐ):", 
            min_value=10_000_000, 
            value=200_000_000, 
            step=10_000_000,
            format="%d",
            key="rev_muc_tieu"
        )
        thoi_gian_nam = st.number_input(
            "Thời gian thực hiện (Năm):", 
            min_value=1, 
            value=3, 
            step=1,
            key="rev_nam"
        )

    with col_rev2:
        lai_suat_dieu_khiet = st.number_input(
            "Lãi suất dự kiến (%/năm):", 
            min_value=0.1, 
            value=6.5, 
            step=0.1,
            format="%.1f",
            key="rev_lai"
        )
        phuong_thuc = st.radio(
            "Cách thức tích lũy:",
            options=["Gửi 1 lần ngay từ đầu", "Gửi góp định kỳ hàng tháng"],
            key="rev_phuong_thuc"
        )

    if st.button("🧮 Tính Số Tiền Cần Gửi", type="primary", use_container_width=True, key="btn_rev"):
        r_nam = lai_suat_dieu_khiet / 100
        n_thang = thoi_gian_nam * 12
        r_thang = r_nam / 12

        st.divider()
        if phuong_thuc == "Gửi 1 lần ngay từ đầu":
            goc_can_gui = muc_tieu / ((1 + r_nam) ** thoi_gian_nam)
            tien_lai_nhan = muc_tieu - goc_can_gui

            st.success(f"💡 Để có **{muc_tieu:,.0f} VNĐ** sau **{thoi_gian_nam} năm** (lãi kép):".replace(",", "."))
            res_r1, res_r2 = st.columns(2)
            with res_r1:
                st.metric("Số tiền gốc cần gửi ngay hôm nay", f"{goc_can_gui:,.0f} VNĐ".replace(",", "."))
            with res_r2:
                st.metric("Tiền lãi ngân hàng hỗ trợ", f"{tien_lai_nhan:,.0f} VNĐ".replace(",", "."))

        else:
            gop_hang_thang = muc_tieu * r_thang / (((1 + r_thang) ** n_thang - 1) * (1 + r_thang))
            tong_goc_gop = gop_hang_thang * n_thang
            tien_lai_nhan = muc_tieu - tong_goc_gop

            st.success(f"💡 Để đạt **{muc_tieu:,.0f} VNĐ** sau **{thoi_gian_nam} năm** ({n_thang} tháng):".replace(",", "."))
            res_r1, res_r2 = st.columns(2)
            with res_r1:
                st.metric("Số tiền cần tiết kiệm mỗi tháng", f"{gop_hang_thang:,.0f} VNĐ".replace(",", "."))
                st.metric("Tổng tiền gốc bạn tự bỏ ra", f"{tong_goc_gop:,.0f} VNĐ".replace(",", "."))
            with res_r2:
                st.metric("Tiền lãi sinh ra", f"{tien_lai_nhan:,.0f} VNĐ".replace(",", "."))

    st.divider()

    # SECTION 2: GIẢ LẬP RÚT TIỀN TRƯỚC HẠN
    st.subheader("🚨 2. Giả Lập Phạt Rút Tiền Trước Hạn")
    st.caption("Rút tiền trước hạn khiến toàn bộ tiền gửi bị tính theo lãi suất Không kỳ hạn (~0.2%/năm).")

    col_rut1, col_rut2 = st.columns(2)
    with col_rut1:
        rut_tien_gui = st.number_input("Số tiền gửi (VNĐ):", value=100_000_000, step=10_000_000, key="rut_tien")
        rut_ky_han = st.number_input("Kỳ hạn đăng ký (Tháng):", value=12, min_value=2, key="rut_ky_han")
    with col_rut2:
        rut_lai_suat = st.number_input("Lãi suất cam kết (%/năm):", value=6.0, step=0.5, key="rut_lai")
        lai_khong_kh = st.number_input("Lãi suất không kỳ hạn (%/năm):", value=0.2, step=0.1, key="rut_lai_khkh")

    thang_rut_som = st.slider("Giả sử bạn phải rút gấp ở tháng thứ:", min_value=1, max_value=int(rut_ky_han), value=int(rut_ky_han // 2))

    # Tính toán
    lai_dung_ky = rut_tien_gui * (rut_lai_suat / 100 / 12) * thang_rut_som
    lai_thuc_nhan = rut_tien_gui * (lai_khong_kh / 100 / 12) * thang_rut_som
    tien_mat_di = lai_dung_ky - lai_thuc_nhan

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.metric("Tổn thất (Số tiền lãi bị mất)", f"{tien_mat_di:,.0f} VNĐ".replace(",", "."))
    with r_col2:
        st.metric("Lãi thực nhận khi rút sớm", f"{lai_thuc_nhan:,.0f} VNĐ".replace(",", "."))

    st.error(f"📉 Nếu rút ở tháng thứ **{thang_rut_som}**, bạn đánh mất **{tien_mat_di:,.0f} VNĐ** tiền lãi do bị tính lãi không kỳ hạn!".replace(",", "."))

# ===================================================================
# TAB 3: TÁC ĐỘNG CỦA LẠM PHÁT (SỨC MUA THỰC TẾ)
# ===================================================================
with tab_inflation:
    st.subheader("🎈 Kiểm Tra Sức Mua Thực Tế Sau Lạm Phát")
    st.write("Lạm phát sẽ làm giảm giá trị thực của tiền lãi nhận được. Hãy kiểm tra xem tài sản của bạn tăng hay giảm sức mua!")

    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        inf_tien_gui = st.number_input("Số tiền gửi (VNĐ):", value=100_000_000, step=10_000_000, key="inf_tien")
        inf_nam = st.number_input("Số năm gửi:", value=3, min_value=1, key="inf_nam")

    with col_inf2:
        inf_lai_suat = st.number_input("Lãi suất tiền gửi (%/năm):", value=6.0, step=0.5, key="inf_lai")
        lam_phat = st.number_input("Tỷ lệ lạm phát dự kiến (%/năm):", value=3.5, step=0.1, key="inf_lam_phat")

    if st.button("📊 Tính Sức Mua Thực", type="primary", use_container_width=True, key="btn_inf"):
        tong_tien_danh_nghia = inf_tien_gui * ((1 + inf_lai_suat / 100) ** inf_nam)
        gia_tri_thuc_te = tong_tien_danh_nghia / ((1 + lam_phat / 100) ** inf_nam)
        lai_thuc_te = gia_tri_thuc_te - inf_tien_gui

        st.divider()
        st.subheader("📊 Kết Quả Phân Tích Sức Mua")

        inf_col1, inf_col2 = st.columns(2)
        with inf_col1:
            st.metric(
                label=f"Tổng tiền danh nghĩa nhận được (sau {inf_nam} năm)", 
                value=f"{tong_tien_danh_nghia:,.0f} VNĐ".replace(",", ".")
            )
            st.metric(
                label="Giá trị thực tế (Sức mua theo giá trị hôm nay)", 
                value=f"{gia_tri_thuc_te:,.0f} VNĐ".replace(",", ".")
            )

        with inf_col2:
            st.metric(
                label="Lãi suất thực (Lãi suất - Lạm phát)", 
                value=f"{inf_lai_suat - lam_phat:.1f}% / năm"
            )
            st.metric(
                label="Tiền lãi thực nhận (Đã trừ trượt giá)", 
                value=f"{lai_thuc_te:,.0f} VNĐ".replace(",", ".")
            )

        if inf_lai_suat > lam_phat:
            st.success("🟢 **Lãi suất thực dương:** Tiền gửi của bạn tăng trưởng nhanh hơn tốc độ tăng giá của hàng hóa.")
        else:
            st.error("🔴 **Lãi suất thực âm:** Sức mua của tiền đang bị suy giảm dù số dư tài khoản vẫn tăng!")
