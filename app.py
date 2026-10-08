import streamlit as st
from datetime import datetime

# ============================================================
# CẤU HÌNH
# ============================================================

st.set_page_config(
    page_title="Quán Trà Chanh - Tính tiền",
    page_icon="🍋",
    layout="wide"
)

# ============================================================
# MENU ĐỒ UỐNG
# ============================================================

MENU = {
    "Trà chanh": 15000,
    "Trà tắc": 15000,
    "Trà đào": 20000,
    "Trà vải": 20000,
    "Trà dâu": 20000,
    "Trà xoài": 20000,
    "Chanh dây": 18000,
    "Nước cam": 20000,
    "Nước ép dưa hấu": 20000,
    "Nước ép thơm": 20000,
    "Sinh tố bơ": 25000,
    "Sinh tố dâu": 25000,
    "Cà phê đen": 15000,
    "Cà phê sữa": 18000,
    "Bạc xỉu": 20000,
    "Pepsi": 12000,
    "Coca Cola": 12000,
    "7Up": 12000,
    "Nước suối": 8000,
}

TOPPING = {
    "Không topping": 0,
    "Trân châu": 5000,
    "Thạch": 5000,
    "Nha đam": 5000,
    "Pudding": 7000,
}

SIZE_PRICE = {
    "M": 0,
    "L": 5000,
}

# ============================================================
# SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

# ============================================================
# HÀM ĐỊNH DẠNG TIỀN
# ============================================================

def money(value):
    return f"{value:,.0f}đ"


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.title("🍋 QUÁN TRÀ CHANH")
st.caption("Hệ thống bán hàng - Tính tiền hóa đơn")

st.divider()

# ============================================================
# THÔNG TIN HÓA ĐƠN
# ============================================================

st.subheader("👤 Thông tin khách hàng")

col1, col2, col3 = st.columns(3)

with col1:
    customer_name = st.text_input(
        "Tên khách hàng",
        placeholder="Khách lẻ"
    )

with col2:
    table_number = st.text_input(
        "Số bàn",
        placeholder="Ví dụ: Bàn 01"
    )

with col3:
    staff_name = st.text_input(
        "Nhân viên",
        placeholder="Tên nhân viên"
    )

st.divider()

# ============================================================
# KHU VỰC BÁN HÀNG
# ============================================================

left, right = st.columns([1, 1])

# ============================================================
# BÊN TRÁI: CHỌN MÓN
# ============================================================

with left:

    st.subheader("🥤 Chọn món")

    drink = st.selectbox(
        "Loại nước",
        list(MENU.keys())
    )

    base_price = MENU[drink]

    size = st.radio(
        "Kích thước",
        ["M", "L"],
        horizontal=True
    )

    topping = st.selectbox(
        "Topping",
        list(TOPPING.keys())
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=100,
        value=1,
        step=1
    )

    unit_price = (
        base_price
        + SIZE_PRICE[size]
        + TOPPING[topping]
    )

    item_total = unit_price * quantity

    st.info(
        f"Đơn giá: **{money(unit_price)}**\n\n"
        f"Thành tiền: **{money(item_total)}**"
    )

    if st.button(
        "➕ THÊM MÓN",
        type="primary",
        use_container_width=True
    ):

        st.session_state.cart.append({
            "drink": drink,
            "size": size,
            "topping": topping,
            "quantity": quantity,
            "unit_price": unit_price,
            "total": item_total
        })

        st.success(f"Đã thêm {drink} vào hóa đơn.")


# ============================================================
# BÊN PHẢI: GIỎ HÀNG
# ============================================================

with right:

    st.subheader("🛒 Hóa đơn tạm")

    if not st.session_state.cart:

        st.info("Chưa có món nào.")

    else:

        subtotal = 0

        for index, item in enumerate(st.session_state.cart):

            subtotal += item["total"]

            st.markdown(
                f"""
**{item['drink']}**

Size: `{item['size']}` | Topping: `{item['topping']}`

{item['quantity']} × {money(item['unit_price'])}
→ **{money(item['total'])}**
"""
            )

            if st.button(
                f"❌ Xóa món {index + 1}",
                key=f"delete_{index}",
                use_container_width=True
            ):
                st.session_state.cart.pop(index)
                st.rerun()

            st.divider()

        # ====================================================
        # GIẢM GIÁ
        # ====================================================

        discount_percent = st.number_input(
            "🏷️ Giảm giá (%)",
            min_value=0,
            max_value=100,
            value=0,
            step=1
        )

        discount = subtotal * discount_percent / 100

        total = subtotal - discount

        st.write(f"**Tạm tính:** {money(subtotal)}")
        st.write(f"**Giảm giá:** -{money(discount)}")

        st.success(
            f"### 💰 TỔNG: {money(total)}"
        )

        # ====================================================
        # TIỀN KHÁCH ĐƯA
        # ====================================================

        customer_payment = st.number_input(
            "💵 Tiền khách đưa",
            min_value=0,
            value=0,
            step=10000
        )

        change = customer_payment - total

        if customer_payment > 0:

            if change >= 0:

                st.success(
                    f"💵 Tiền thừa: **{money(change)}**"
                )

            else:

                st.error(
                    f"⚠️ Khách còn thiếu: "
                    f"**{money(abs(change))}**"
                )

        # ====================================================
        # THANH TOÁN
        # ====================================================

        can_pay = (
            customer_payment >= total
        )

        if st.button(
            "💳 THANH TOÁN",
            type="primary",
            use_container_width=True,
            disabled=not can_pay
        ):

            now = datetime.now()

            invoice_id = now.strftime(
                "%Y%m%d%H%M%S"
            )

            st.session_state.invoice = {
                "id": invoice_id,
                "date": now.strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),
                "customer": (
                    customer_name
                    if customer_name.strip()
                    else "Khách lẻ"
                ),
                "table": (
                    table_number
                    if table_number.strip()
                    else "Không có"
                ),
                "staff": (
                    staff_name
                    if staff_name.strip()
                    else "Nhân viên"
                ),
                "items": st.session_state.cart.copy(),
                "subtotal": subtotal,
                "discount_percent": discount_percent,
                "discount": discount,
                "total": total,
                "payment": customer_payment,
                "change": change
            }

            # Xóa giỏ hàng sau khi thanh toán
            st.session_state.cart = []

            st.rerun()


# ============================================================
# HÓA ĐƠN SAU KHI THANH TOÁN
# ============================================================

if st.session_state.invoice:

    invoice = st.session_state.invoice

    st.divider()

    st.header("🧾 HÓA ĐƠN THANH TOÁN")

    # ========================================================
    # THÔNG TIN SHOP
    # ========================================================

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px;
        ">

        <h1>🍋 QUÁN TRÀ CHANH</h1>

        <p>
        <b>HÓA ĐƠN THANH TOÁN</b>
        </p>

        <p>
        Cảm ơn quý khách đã ủng hộ!
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # THÔNG TIN HÓA ĐƠN
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Mã hóa đơn:** {invoice['id']}"
        )

        st.write(
            f"**Thời gian:** {invoice['date']}"
        )

        st.write(
            f"**Khách hàng:** {invoice['customer']}"
        )

    with col2:

        st.write(
            f"**Số bàn:** {invoice['table']}"
        )

        st.write(
            f"**Nhân viên:** {invoice['staff']}"
        )

    st.divider()

    # ========================================================
    # DANH SÁCH MÓN
    # ========================================================

    st.subheader("🥤 Chi tiết đơn hàng")

    for item in invoice["items"]:

        col1, col2, col3, col4 = st.columns(
            [3, 1, 1, 2]
        )

        with col1:
            st.write(
                f"**{item['drink']}**"
            )
            st.caption(
                f"Size {item['size']} - "
                f"{item['topping']}"
            )

        with col2:
            st.write(
                f"x{item['quantity']}"
            )

        with col3:
            st.write(
                money(item["unit_price"])
            )

        with col4:
            st.write(
                f"**{money(item['total'])}**"
            )

    st.divider()

    # ========================================================
    # TỔNG TIỀN
    # ========================================================

    col1, col2 = st.columns([2, 1])

    with col2:

        st.write(
            f"**Tạm tính:** "
            f"{money(invoice['subtotal'])}"
        )

        st.write(
            f"**Giảm giá:** "
            f"-{money(invoice['discount'])}"
        )

        st.markdown(
            f"""
### 💰 Tổng thanh toán
# {money(invoice['total'])}
"""
        )

        st.write(
            f"**Khách đưa:** "
            f"{money(invoice['payment'])}"
        )

        st.write(
            f"**Tiền thừa:** "
            f"{money(invoice['change'])}"
        )

    st.divider()

    # ========================================================
    # TRẠNG THÁI THANH TOÁN
    # ========================================================

    st.success(
        "✅ THANH TOÁN THÀNH CÔNG"
    )

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:20px;
        ">

        <h3>❤️ CẢM ƠN QUÝ KHÁCH ❤️</h3>

        <p>
        Hẹn gặp lại quý khách!
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # NÚT TẠO HÓA ĐƠN MỚI
    # ========================================================

    if st.button(
        "🆕 TẠO HÓA ĐƠN MỚI",
        use_container_width=True
    ):

        st.session_state.invoice = None

        st.rerun()
