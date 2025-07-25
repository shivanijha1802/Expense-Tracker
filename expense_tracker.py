import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from datetime import datetime
import os
import json

# === Setting the page ===
st.set_page_config(page_title="Expense Tracker", layout="wide")

placeholder_alert = st.empty()

# === Setting title of the page ===
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>💸 Expense Tracker</h1>
""", unsafe_allow_html=True)

# === The file path to save expenses ===
save_path = 'expenses_data.csv'

# === To upload CSV file ===
with st.expander("📂 Upload Expense CSV File"):
    upload_file = st.file_uploader("Choose a CSV file", type=['csv'])

# === Using session_state to preserve the data ===
if 'expense_data' not in st.session_state:
    if os.path.exists(save_path):
        st.session_state.expense_data = pd.read_csv(save_path, parse_dates=['Date'])
    else:
        st.session_state.expense_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
expense_data = st.session_state.expense_data 

# === Manual expense input form ===
st.subheader("📝 Add Expense Manaually")

with st.form("expense_entry_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date", value=datetime.today())
    with col2:
        category = st.text_input("Category", placeholder="e.g., Food, Transport")
    with col3:
        amount = st.number_input("Amount", min_value=0.0, step=1.0)

    description = st.text_input("Description", placeholder="e.g., Dinner with family, Go on a trip")
    submitted = st.form_submit_button("➕ Add Expense")

    if submitted:
        new_row = {"Date": pd.to_datetime(date), "Category": category, "Amount": amount, "Description": description}
        st.session_state.expense_data = pd.concat([st.session_state.expense_data, pd.DataFrame([new_row])], ignore_index=True)
        st.session_state.expense_data.to_csv(save_path, index=False)
        st.success("Expense Added Successfully!")

# === To combine the CSV & Manaul Data ===
if upload_file:
    csv_data = pd.read_csv(upload_file)

    # === Converting date to datetime column ===
    csv_data['Date'] = pd.to_datetime(csv_data['Date'], errors='coerce')
    csv_data.dropna(subset=['Date'], inplace=True)

    # === Add the description if not ===
    if 'Description' not in csv_data.columns:
        csv_data['Description'] = "No Description"

    # === Combining csv & manual data ===
    st.session_state.expense_data = pd.concat([csv_data, st.session_state.expense_data], ignore_index=True)
    st.session_state.expense_data.to_csv(save_path, index=False)
    expense_data = st.session_state.expense_data

# === If data is there already, to continue the processing ===
if not expense_data.empty:
    # === Applying the fileters ===
    st.sidebar.header("🔎 Filters")

    # === Convert datetime ===
    expense_data['Date'] = pd.to_datetime(expense_data['Date'])

    # === Date range filter ===
    min_date = expense_data['Date'].min()
    max_date = expense_data['Date'].max()
    start_date, end_date = st.sidebar.date_input("Select Date Range:", [min_date, max_date])

    # === Category filter ===
    categories = expense_data['Category'].unique().tolist()
    selected_catgry = st.sidebar.multiselect("Select Categories: ", categories, default=categories)

    # === Apply filters ===
    filtered_data = expense_data[
        (expense_data['Date'] >= pd.to_datetime(start_date)) & 
        (expense_data['Date'] <= pd.to_datetime(end_date)) & 
        (expense_data['Category'].isin(selected_catgry))
    ]

    # === Displaying the filterd data ===
    st.subheader("📋 Filtered Expenses")

    df_display = filtered_data.copy()
    df_display['Date'] = df_display['Date'].dt.strftime('%d %B %Y')
    st.dataframe(df_display)

    for i, row in filtered_data.reset_index().iterrows():
        col1, col2 = st.columns([6, 1])
        with col1:
            clean_date = row['Date'].strftime('%d %B %Y')
            st.write(f"**{clean_date}** | {row['Category']} | ₹{row['Amount']} | {row['Description']}")
        with col2:
            if st.button("🗑️ Delete", key=f"del_{row['index']}"):
                st.session_state.expense_data.drop(index=row['index'], inplace=True)
                st.session_state.expense_data.reset_index(drop=True, inplace=True)
                st.session_state.expense_data.to_csv(save_path, index=False)
                st.rerun()

    # === To show monthly summary ===
    st.subheader("📊 Monthly Summary Dashboard")
    filtered_data['Month'] = filtered_data['Date'].dt.to_period('M')
    monthly_summary = filtered_data.groupby('Month')['Amount'].sum().reset_index()

    fig1, ax1 = plt.subplots()
    ax1.bar(monthly_summary['Month'].astype(str), monthly_summary['Amount'], color='lightgreen')
    ax1.set_title("Month-Wise Expenses")
    ax1.set_ylabel("Total Amount")
    st.pyplot(fig1)

    st.write("📊 Monthly Summary Table")
    summary_display = monthly_summary.copy()
    summary_display['Month'] = summary_display['Month'].astype(str)
    st.dataframe(summary_display)

    # === Category Pie Chart ===
    st.subheader("📈 Category-wise Expense Distribution")
    ctgry_summary = filtered_data.groupby('Category')['Amount'].sum()
    fig2, ax2 = plt.subplots()
    ax2.pie(ctgry_summary, labels=ctgry_summary.index, autopct='%1.1f%%', startangle=140)
    ax2.axis('equal')
    st.pyplot(fig2)
    print("\n\n")

    # === Top spending categories ===
    st.subheader("🔥 Top 5 Spending Categories")
    top_ctgrs = ctgry_summary.sort_values(ascending=False).head(5)
    st.bar_chart(top_ctgrs)

    # === Budget alert ===
    BUDGET_FILE = "budget.json"

    # Load or save budget
    def load_budget(): return json.load(open(BUDGET_FILE))["budget"] if os.path.exists(BUDGET_FILE) else 0.0
    def save_budget(b): json.dump({"budget": b}, open(BUDGET_FILE, "w"))

    st.session_state['budget'] = st.session_state.get('budget', load_budget())

    st.sidebar.markdown("### 💰 Monthly Budget")
    budget_input = st.sidebar.number_input("Set Monthly Budget", min_value=0.0, step=100.0, value=st.session_state['budget'])

    if st.sidebar.button("💾 Save Budget"):
        st.session_state['budget'] = budget_input
        save_budget(budget_input)
        st.sidebar.success(f"✅ Budget saved: ₹{budget_input}")

    # Budget alert
    if st.session_state['budget'] > 0:
        over = monthly_summary[monthly_summary['Amount'] > st.session_state['budget']]
        if not over.empty:
            placeholder_alert.warning(f"⚠️ Budget exceeded in: {', '.join(over['Month'].astype(str))}")
        else:
            placeholder_alert.success("✅ All months are within your Budget!")

    # === Export to Excel ===
    st.subheader("📤 Export Expenses Report to Excel")

    def convert_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Expenses')
            output.seek(0)
        return output

    if not filtered_data.empty:
        excel_file = convert_to_excel(filtered_data)
        st.download_button(
            label="⬇ Download Excel Expenses Report",
            data=excel_file,
            file_name="Expense_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No data to export.")

else:
    st.info("ℹ️ Please upload a CSV file or add Expenses using the manual form.")

# === Footer ===
st.markdown("---")
st.caption("🚀 Built by Python Intern Shivani | Streamlit + Pandas + Matplotlib")