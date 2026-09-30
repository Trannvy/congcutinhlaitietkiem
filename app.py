import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 Máy tính lãi suất tiết kiệm")
st.caption("Tính lãi theo phương pháp lãi đơn hoặc lãi kép")

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin khoản gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

hinh_thuc_tinh = st.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh_lai = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 Tính lãi", type="primary", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    r = lai_suat / 100

    # Kỳ hạn tính theo năm
    so_nam = ky_han / 12

    # Lãi suất theo tháng
    lai_suat_thang = r / 12

    # -------------------------
    # LÃI ĐƠN
    # -------------------------
    if hinh_thuc_tinh == "Lãi đơn":

        tong_tien_lai = so_tien * r * so_nam
        tong_goc_lai = so_tien + tong_tien_lai

        # Tiền lãi định kỳ
        if hinh_thuc_lanh_lai == "Lãnh lãi theo tháng":
            tien_lai_dinh_ky = so_tien * lai_suat_thang

        elif hinh_thuc_lanh_lai == "Lãnh lãi theo quý":
            tien_lai_dinh_ky = so_tien * r / 4

        else:
            tien_lai_dinh_ky = tong_tien_lai

    # -------------------------
    # LÃI KÉP
    # -------------------------
    else:

        if hinh_thuc_lanh_lai == "Lãnh lãi theo tháng":

            # Ghép lãi hàng tháng
            so_ky = ky_han

            tong_goc_lai = so_tien * (1 + lai_suat_thang) ** so_ky
            tong_tien_lai = tong_goc_lai - so_tien

            # Lãi của kỳ đầu tiên
            tien_lai_dinh_ky = so_tien * lai_suat_thang

        elif hinh_thuc_lanh_lai == "Lãnh lãi theo quý":

            # Ghép lãi hàng quý
            so_ky = ky_han / 3
            lai_suat_quy = r / 4

            tong_goc_lai = so_tien * (1 + lai_suat_quy) ** so_ky
            tong_tien_lai = tong_goc_lai - so_tien

            # Lãi của quý đầu tiên
            tien_lai_dinh_ky = so_tien * lai_suat_quy

        else:

            # Lãnh lãi cuối kỳ: ghép lãi theo tháng
            so_ky = ky_han

            tong_goc_lai = so_tien * (1 + lai_suat_thang) ** so_ky
            tong_tien_lai = tong_goc_lai - so_tien

            tien_lai_dinh_ky = tong_tien_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.divider()
    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(tien_lai_dinh_ky)
        )

    with col2:
        st.metric(
            "💰 Tổng tiền lãi",
            format_money(tong_tien_lai)
        )

    st.metric(
        "🏦 Tổng tiền gốc + lãi",
        format_money(tong_goc_lai)
    )

    # =========================
    # THÔNG TIN KHOẢN GỬI
    # =========================
    st.divider()
    st.subheader("📝 Chi tiết khoản gửi")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Số tiền gửi:** {format_money(so_tien)}")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")

    with col2:
        st.write(f"**Phương pháp:** {hinh_thuc_tinh}")
        st.write(f"**Hình thức nhận lãi:** {hinh_thuc_lanh_lai}")

    # =========================
    # CÔNG THỨC
    # =========================
    with st.expander("📐 Xem công thức tính"):

        if hinh_thuc_tinh == "Lãi đơn":
            st.latex(
                r"I = P \times r \times t"
            )
            st.write(
                "Trong đó: P là tiền gốc, r là lãi suất năm, "
                "t là số năm gửi."
            )

        else:
            if hinh_thuc_lanh_lai == "Lãnh lãi theo tháng":
                st.latex(
                    r"A = P\left(1+\frac{r}{12}\right)^n"
                )
                st.write(
                    "Lãi được nhập vào gốc hàng tháng."
                )

            elif hinh_thuc_lanh_lai == "Lãnh lãi theo quý":
                st.latex(
                    r"A = P\left(1+\frac{r}{4}\right)^n"
                )
                st.write(
                    "Lãi được nhập vào gốc hàng quý."
                )

            else:
                st.latex(
                    r"A = P\left(1+\frac{r}{12}\right)^n"
                )
                st.write(
                    "Lãi được cộng dồn theo tháng và nhận toàn bộ "
                    "gốc + lãi khi kết thúc kỳ hạn."
                )

# =========================
# FOOTER
# =========================
st.divider()
st.caption(
    "⚠️ Kết quả mang tính chất tham khảo. "
    "Lãi suất và phương thức tính thực tế có thể khác tùy ngân hàng."
)
