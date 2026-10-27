import streamlit as st


class ATM:
    def __init__(self):
        self.pin = ""
        self.balance = 0

    def create_pin(self, pin, balance):
        self.pin = pin
        self.balance = balance

    def verify_pin(self, pin):
        return self.pin != "" and pin == self.pin

    def change_pin(self, old_pin, new_pin):
        if self.verify_pin(old_pin):
            self.pin = new_pin
            return True
        return False

    def withdraw(self, pin, amount):
        if not self.verify_pin(pin):
            return "invalid_pin"
        if amount > self.balance:
            return "insufficient"
        self.balance -= amount
        return "ok"


# Streamlit re-runs this script on every click, so the ATM object
# must be stored in session_state to keep pin and balance.
if "atm" not in st.session_state:
    st.session_state.atm = ATM()

atm = st.session_state.atm

st.title("🏧 ATM Machine")

choice = st.sidebar.radio(
    "Menu",
    ["Create PIN", "Change PIN", "Check Balance", "Withdrawal"],
)

# ---------- 1) Create PIN ----------
if choice == "Create PIN":
    st.subheader("Create PIN")
    with st.form("create_pin_form"):
        pin = st.text_input("Enter your PIN", type="password")
        balance = st.number_input("Enter balance", min_value=0, step=100)
        submitted = st.form_submit_button("Create PIN")
    if submitted:
        if not pin:
            st.error("PIN cannot be empty.")
        else:
            atm.create_pin(pin, int(balance))
            st.success("PIN created successfully")

# ---------- 2) Change PIN ----------
elif choice == "Change PIN":
    st.subheader("Change PIN")
    with st.form("change_pin_form"):
        old_pin = st.text_input("Enter old PIN", type="password")
        new_pin = st.text_input("Enter new PIN", type="password")
        submitted = st.form_submit_button("Change PIN")
    if submitted:
        if not new_pin:
            st.error("New PIN cannot be empty.")
        elif atm.change_pin(old_pin, new_pin):
            st.success("PIN changed successfully")
        else:
            st.error("Not valid. Wrong PIN (or no PIN created yet).")

# ---------- 3) Check Balance ----------
elif choice == "Check Balance":
    st.subheader("Check Balance")
    with st.form("balance_form"):
        pin = st.text_input("Enter PIN", type="password")
        submitted = st.form_submit_button("Check")
    if submitted:
        if atm.verify_pin(pin):
            st.info(f"Your balance is: ₹{atm.balance}")
        else:
            st.error("Wrong PIN (or no PIN created yet).")

# ---------- 4) Withdrawal ----------
elif choice == "Withdrawal":
    st.subheader("Withdrawal")
    with st.form("withdraw_form"):
        pin = st.text_input("Enter PIN", type="password")
        amount = st.number_input("Enter amount", min_value=0, step=100)
        submitted = st.form_submit_button("Withdraw")
    if submitted:
        result = atm.withdraw(pin, int(amount))
        if result == "ok":
            st.success(f"Withdrawal successful. Balance is ₹{atm.balance}")
        elif result == "invalid_pin":
            st.error("Wrong PIN (or no PIN created yet).")
        else:
            st.error("Insufficient balance.")