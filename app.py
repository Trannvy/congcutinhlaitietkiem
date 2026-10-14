
import streamlit as st

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Ứng Dụng Tính Lãi Gửi Tiết Kiệm")
st.image("funny cat meme.jpg")
st.write(
    "Nhập thông tin tiền gửi bên dưới để tính toán lãi tiết kiệm "
    "theo **lãi đơn** hoặc **lãi kép**."
)

st.divider()

# ==============================
# NHẬP THÔNG TIN TIỀN GỬI
# ==============================
col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "Số tiền gửi (VNĐ):",
        min_value=1_000_000,
        value=100_000_000,
        step=5_000_000,
        format="%d"
    )

    ky_han_thang = st.number_input(
        "Kỳ hạn gửi (Tháng):",
        min_value=1,
        value=12,
        step=1
    )

with col2:
    lai_suat_nam = st.number_input(
        "Lãi suất (%/năm):",
        min_value=0.1,
        max_value=20.0,
        value=6.0,
        step=0.1,
        format="%.1f"
    )

    loai_lai = st.selectbox(
        "Phương thức tính lãi:",
        options=["Lãi đơn", "Lãi kép"]
    )

hinh_thuc_lanh = st.selectbox(
    "Hình thức lãnh lãi:",
    options=[
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# ==============================
# TÍNH TOÁN LÃI TIẾT KIỆM
# ==============================
if st.button(
    "🚀 Tính Tiền Lãi",
    type="primary",
    use_container_width=True
):
    r_thang = (lai_suat_nam / 100) / 12

    # Xác định chu kỳ lãnh lãi
    if hinh_thuc_lanh == "Lãnh lãi theo tháng":
        m = 1
    elif hinh_thuc_lanh == "Lãnh lãi theo quý":
        m = 3
    else:
        m = ky_han_thang

    # Kiểm tra kỳ hạn có chia hết cho chu kỳ lãnh lãi
    if (
        ky_han_thang % m != 0
        and hinh_thuc_lanh != "Lãnh lãi cuối kỳ"
    ):
        st.warning(
            f"⚠️ Kỳ hạn gửi ({ky_han_thang} tháng) không chia hết "
            f"cho chu kỳ {hinh_thuc_lanh.lower()}. "
            "Kết quả tính theo số chu kỳ chẵn."
        )

    so_chu_ky = ky_han_thang // m

    if loai_lai == "Lãi đơn":
        # Lãi đơn: tính trên vốn gốc ban đầu
        lai_dinh_ky = so_tien_gui * r_thang * m
        tong_lai = lai_dinh_ky * so_chu_ky
        tong_tien = so_tien_gui + tong_lai

    else:
        # Lãi kép: lãi nhập gốc qua từng chu kỳ
        r_chu_ky = r_thang * m

        tong_tien = so_tien_gui * (
            (1 + r_chu_ky) ** so_chu_ky
        )

        tong_lai = tong_tien - so_tien_gui

        lai_dinh_ky = (
            tong_lai / so_chu_ky
            if so_chu_ky > 0
            else 0
        )

    # ==============================
    # HIỂN THỊ KẾT QUẢ GỐC
    # ==============================
    st.divider()
    st.subheader("📊 Kết Quả Tính Toán")

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

        label_dinh_ky = (
            "Tiền lãi nhận mỗi kỳ"
            if loai_lai == "Lãi đơn"
            else "Lãi nhận trung bình/kỳ"
        )

        st.metric(
            label=f"{label_dinh_ky} ({m} tháng/kỳ)",
            value=f"{lai_dinh_ky:,.0f} VNĐ".replace(",", ".")
        )

    # ==============================
    # BẢNG CHI TIẾT CÁC KỲ NHẬN LÃI
    # ==============================
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
                "Tiền gốc đầu kỳ (VNĐ)": (
                    f"{goc_dau_ky:,.0f}".replace(",", ".")
                ),
                "Lãi nhận được (VNĐ)": (
                    f"{lai_ky:,.0f}".replace(",", ".")
                ),
                "Tổng tích lũy (VNĐ)": (
                    f"{(
                        goc_cuoi_ky
                        if loai_lai == 'Lãi kép'
                        else so_tien_gui + lai_ky * i
                    ):,.0f}".replace(",", ".")
                )
            })

            goc_dau_ky = goc_cuoi_ky

        st.dataframe(
            lich_trinh,
            use_container_width=True
        )

    # ==================================================
    # TÍNH NĂNG MỚI 1: ĐỒNG HỒ SỨC MUA TƯƠNG LAI
    # ==================================================
    st.divider()
    st.subheader("🔮 Đồng hồ sức mua tương lai")

    st.write(
        "Mô phỏng sức mua của khoản tiền cuối kỳ sau khi "
        "xét đến mức lạm phát giả định."
    )

    lam_phat = st.number_input(
        "Lạm phát giả định (%/năm):",
        min_value=0.0,
        max_value=30.0,
        value=3.5,
        step=0.5,
        help=(
            "Mức lạm phát giả định để mô phỏng, "
            "không phải dự báo chắc chắn."
        ),
        key="lam_phat_moi"
    )

    so_nam = ky_han_thang / 12

    # Quy đổi số tiền cuối kỳ về sức mua theo giá hiện tại
    suc_mua_hien_tai = tong_tien / (
        (1 + lam_phat / 100) ** so_nam
    )

    chenh_lech_suc_mua = tong_tien - suc_mua_hien_tai

    mua_col1, mua_col2 = st.columns(2)

    with mua_col1:
        st.metric(
            "Số tiền cuối kỳ",
            f"{tong_tien:,.0f} VNĐ".replace(",", ".")
        )

    with mua_col2:
        st.metric(
            "Sức mua quy đổi về hôm nay",
            f"{suc_mua_hien_tai:,.0f} VNĐ".replace(",", "."),
            delta=(
                f"-{chenh_lech_suc_mua:,.0f} VNĐ".replace(",", ".")
            ),
            delta_color="inverse"
        )

    st.caption(
        f"Giả sử lạm phát duy trì ở mức {lam_phat:.1f}%/năm "
        f"trong {so_nam:.2f} năm. "
        "Chênh lệch trên là giá trị quy đổi sức mua, "
        "không phải khoản tiền bị trừ khỏi tài khoản."
    )

    # ==================================================
    # TÍNH NĂNG MỚI 2: KIỂM TRA MỤC TIÊU TÀI CHÍNH
    # ==================================================
    st.divider()
    st.subheader("🎯 Kiểm tra mục tiêu tài chính")

    muc_tieu = st.number_input(
        "Mục tiêu tài chính (VNĐ):",
        min_value=1_000_000,
        value=120_000_000,
        step=5_000_000,
        format="%d",
        key="muc_tieu_moi"
    )

    tien_con_thieu = max(0, muc_tieu - tong_tien)

    phan_tram_muc_tieu = min(
        100.0,
        tong_tien / muc_tieu * 100
    )

    st.progress(phan_tram_muc_tieu / 100)

    st.write(
        f"**Mức độ hoàn thành mục tiêu: "
        f"{phan_tram_muc_tieu:.1f}%**"
    )

    if tong_tien >= muc_tieu:
        st.success(
            "🎉 Với giả định tính toán hiện tại, "
            "bạn dự kiến đạt mục tiêu tài chính!"
        )

        st.write(
            "Số tiền vượt mục tiêu: "
            f"{tong_tien - muc_tieu:,.0f} VNĐ".replace(",", ".")
        )

    else:
        st.warning(
            "Khoản tiền gửi dự kiến chưa đạt mục tiêu tài chính."
        )

        st.write(
            "Số tiền còn thiếu: "
            f"{tien_con_thieu:,.0f} VNĐ".replace(",", ".")
        )

    st.caption(
        "Các kết quả là mô phỏng dựa trên thông số đã nhập. "
        "Lãi suất thực tế, cách nhập lãi gốc và điều kiện rút trước "
        "hạn có thể khác tùy sản phẩm tiền gửi của ngân hàng."
    )
