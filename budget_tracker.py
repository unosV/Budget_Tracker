import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import hashlib
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Smart Budget Tracker", 
    page_icon="💰", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# File paths
USERS_FILE = Path("users.json")

# Default expense categories
DEFAULT_CATEGORIES = [
    "Rent/Mortgage", "Utilities", "Groceries", "Transport", 
    "Entertainment", "Healthcare", "Insurance", "Savings",
    "Debt Repayment", "Dining Out", "Shopping", "Other"
]

# ============= AUTHENTICATION FUNCTIONS =============

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load user credentials"""
    if USERS_FILE.exists():
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save user credentials"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_user_data_file(username):
    """Get data file path for specific user"""
    return Path(f"budget_data_{username}.json")

def load_user_data(username):
    """Load budget data for specific user"""
    data_file = get_user_data_file(username)
    if data_file.exists():
        with open(data_file, 'r') as f:
            return json.load(f)
    return {}

def save_user_data(username, data):
    """Save budget data for specific user"""
    data_file = get_user_data_file(username)
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

def signup(username, password, email):
    """Create new user account"""
    users = load_users()
    
    if username in users:
        return False, "Username already exists!"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters!"
    
    users[username] = {
        'password': hash_password(password),
        'email': email,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    save_users(users)
    
    # Initialize empty budget data for new user
    save_user_data(username, {})
    
    return True, "Account created successfully! Please login."

def login(username, password):
    """Authenticate user"""
    users = load_users()
    
    if username not in users:
        return False, "Username not found!"
    
    if users[username]['password'] != hash_password(password):
        return False, "Incorrect password!"
    
    return True, "Login successful!"

def logout():
    """Logout user"""
    for key in ['logged_in', 'username', 'data', 'current_month']:
        if key in st.session_state:
            del st.session_state[key]

# ============= BUDGET FUNCTIONS =============

def get_month_key():
    """Get current month key in YYYY-MM format"""
    return datetime.now().strftime("%Y-%m")

def initialize_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        if 'data' not in st.session_state:
            st.session_state.data = load_user_data(st.session_state.username)
        if 'current_month' not in st.session_state:
            st.session_state.current_month = get_month_key()

def create_pie_chart(expenses_data, title):
    """Create expense breakdown pie chart - FIXED LAYOUT"""
    df = pd.DataFrame(list(expenses_data.items()), columns=['Category', 'Amount'])
    df = df[df['Amount'] > 0]
    
    colors = px.colors.qualitative.Set2
    
    fig = px.pie(df, values='Amount', names='Category', 
                 hole=0.4, color_discrete_sequence=colors)
    fig.update_traces(
        textposition='inside', 
        textinfo='percent',
        textfont_size=12
    )
    fig.update_layout(
        height=500,
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            y=0.98,
            font=dict(size=18)
        ),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=11)
        ),
        margin=dict(l=20, r=180, t=60, b=20)
    )
    return fig

def create_bar_chart(expenses_data, income, title):
    """Create income vs expenses bar chart - FIXED LAYOUT"""
    total_expenses = sum(expenses_data.values())
    savings = income - total_expenses
    
    fig = go.Figure(data=[
        go.Bar(
            name='Income', 
            x=['Budget'], 
            y=[income], 
            marker_color='#2ecc71',
            text=[f'${income:,.0f}'],
            textposition='outside'
        ),
        go.Bar(
            name='Expenses', 
            x=['Budget'], 
            y=[total_expenses], 
            marker_color='#e74c3c',
            text=[f'${total_expenses:,.0f}'],
            textposition='outside'
        ),
        go.Bar(
            name='Savings', 
            x=['Budget'], 
            y=[savings], 
            marker_color='#3498db',
            text=[f'${savings:,.0f}'],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            y=0.98,
            font=dict(size=18)
        ),
        barmode='group',
        height=500,
        yaxis_title='Amount ($)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        margin=dict(l=60, r=60, t=70, b=80)
    )
    return fig

def create_trend_chart(data, metric):
    """Create month-over-month trend line chart"""
    months = []
    values = []
    
    for month, month_data in sorted(data.items()):
        months.append(month)
        if metric == 'savings':
            income = month_data.get('income', 0)
            expenses = sum(month_data.get('expenses', {}).values())
            values.append(income - expenses)
        elif metric == 'expenses':
            values.append(sum(month_data.get('expenses', {}).values()))
        elif metric == 'debt':
            values.append(month_data.get('debt', 0))
    
    colors = {
        'savings': '#2ecc71',
        'expenses': '#e74c3c',
        'debt': '#f39c12'
    }
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, 
        y=values, 
        mode='lines+markers',
        name=metric.capitalize(),
        line=dict(width=4, color=colors.get(metric, '#3498db')),
        marker=dict(size=12, color=colors.get(metric, '#3498db'))
    ))
    
    fig.update_layout(
        title=dict(
            text=f"{metric.capitalize()} Trend",
            x=0.5,
            xanchor='center',
            font=dict(size=18)
        ),
        xaxis_title="Month",
        yaxis_title=f"Amount ($)",
        height=450,
        font=dict(size=14),
        margin=dict(l=60, r=60, t=70, b=60)
    )
    return fig

def calculate_insights(current_data, historical_data):
    """Generate smart insights"""
    insights = []
    
    current_income = current_data.get('income', 0)
    current_expenses = sum(current_data.get('expenses', {}).values())
    current_savings = current_income - current_expenses
    current_debt = current_data.get('debt', 0)
    
    if current_income > 0:
        savings_rate = (current_savings / current_income) * 100
        if savings_rate > 20:
            insights.append(f"🎉 Great job! You're saving {savings_rate:.1f}% of your income.")
        elif savings_rate > 10:
            insights.append(f"💪 Good! You're saving {savings_rate:.1f}%. Try to reach 20%.")
        else:
            insights.append(f"⚠️ You're only saving {savings_rate:.1f}%. Aim for at least 10-20%.")
    
    if current_expenses > 0:
        expenses_dict = current_data.get('expenses', {})
        top_expense = max(expenses_dict.items(), key=lambda x: x[1])
        insights.append(f"📊 Your highest expense is {top_expense[0]} at ${top_expense[1]:,.2f}")
    
    if len(historical_data) > 1:
        sorted_months = sorted(historical_data.keys())
        if len(sorted_months) >= 2:
            prev_month = sorted_months[-2]
            prev_expenses = sum(historical_data[prev_month].get('expenses', {}).values())
            
            if current_expenses > prev_expenses:
                change = ((current_expenses - prev_expenses) / prev_expenses) * 100
                insights.append(f"📈 Expenses increased by {change:.1f}% from last month")
            elif current_expenses < prev_expenses:
                change = ((prev_expenses - current_expenses) / prev_expenses) * 100
                insights.append(f"📉 Great! Expenses decreased by {change:.1f}% from last month")
    
    if current_debt > 0 and current_savings > 0:
        months_to_clear = current_debt / current_savings
        insights.append(f"💡 At your current savings rate, you can clear your debt in {months_to_clear:.1f} months")
    
    if current_income > 0:
        recommended_expenses = current_income * 0.8
        if current_expenses > recommended_expenses:
            insights.append(f"💰 Try to reduce expenses to ${recommended_expenses:,.2f} (80% of income)")
    
    return insights

# ============= MAIN APP =============

initialize_session_state()

# LOGIN/SIGNUP PAGE
if not st.session_state.logged_in:
    st.title("💰 Smart Budget Tracker")
    st.markdown("### Personal Finance Management with Multi-User Support")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary"):
            if login_username and login_password:
                success, message = login(login_username, login_password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.session_state.data = load_user_data(login_username)
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please enter both username and password")
    
    with tab2:
        st.subheader("Create New Account")
        
        signup_username = st.text_input("Choose Username", key="signup_username")
        signup_email = st.text_input("Email (optional)", key="signup_email")
        signup_password = st.text_input("Choose Password (min 6 characters)", type="password", key="signup_password")
        signup_password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
        
        if st.button("Create Account", type="primary"):
            if signup_username and signup_password and signup_password_confirm:
                if signup_password != signup_password_confirm:
                    st.error("Passwords don't match!")
                else:
                    success, message = signup(signup_username, signup_password, signup_email)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            else:
                st.warning("Please fill in all required fields")
    
    st.markdown("---")
    st.info("👥 Each user has their own private budget data. Your information is stored securely.")

# MAIN BUDGET TRACKER (Only shown when logged in)
else:
    # Header with logout
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title(f"💰 Smart Budget Tracker")
        st.markdown(f"### Welcome back, **{st.session_state.username}**!")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            logout()
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("Month Selection")
    all_months = sorted(list(st.session_state.data.keys()) + [get_month_key()])
    all_months = sorted(list(set(all_months)), reverse=True)
    
    selected_month = st.sidebar.selectbox(
        "Select Month",
        all_months,
        index=0 if get_month_key() in all_months else len(all_months)-1
    )
    
    st.session_state.current_month = selected_month
    
    if selected_month not in st.session_state.data:
        st.session_state.data[selected_month] = {
            'income': 0,
            'expenses': {cat: 0 for cat in DEFAULT_CATEGORIES},
            'debt': 0
        }
    
    current_data = st.session_state.data[selected_month]
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📝 Budget Input", "📊 Current Month", "📈 Trends & Insights"])
    
    # TAB 1: Input
    with tab1:
        st.header(f"Budget for {selected_month}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💵 Income")
            income = st.number_input(
                "Monthly Income (after tax)",
                min_value=0.0,
                value=float(current_data.get('income', 0)),
                step=100.0,
                key='income_input'
            )
            current_data['income'] = income
            
            st.subheader("💳 Debt")
            debt = st.number_input(
                "Total Outstanding Debt",
                min_value=0.0,
                value=float(current_data.get('debt', 0)),
                step=100.0,
                key='debt_input'
            )
            current_data['debt'] = debt
        
        with col2:
            st.subheader("💸 Expenses")
            
            if 'expenses' not in current_data:
                current_data['expenses'] = {cat: 0 for cat in DEFAULT_CATEGORIES}
            
            for category in DEFAULT_CATEGORIES:
                current_data['expenses'][category] = st.number_input(
                    category,
                    min_value=0.0,
                    value=float(current_data['expenses'].get(category, 0)),
                    step=10.0,
                    key=f'expense_{category}'
                )
        
        # Add custom category
        st.markdown("---")
        st.subheader("➕ Add Custom Category")
        col_a, col_b = st.columns([3, 1])
        with col_a:
            custom_category = st.text_input("Category Name", key='custom_cat_name')
        with col_b:
            custom_amount = st.number_input("Amount", min_value=0.0, step=10.0, key='custom_cat_amount')
        
        if st.button("Add Category") and custom_category:
            current_data['expenses'][custom_category] = custom_amount
            st.success(f"Added {custom_category}!")
            st.rerun()
        
        # Save button
        st.markdown("---")
        if st.button("💾 Save Month Data", type="primary"):
            save_user_data(st.session_state.username, st.session_state.data)
            st.success(f"✅ Data saved for {selected_month}!")
    
    # TAB 2: Current Month Analysis
    with tab2:
        st.header(f"Analysis for {selected_month}")
        
        total_expenses = sum(current_data.get('expenses', {}).values())
        total_savings = income - total_expenses
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💵 Income", f"${income:,.2f}")
        with col2:
            st.metric("💸 Expenses", f"${total_expenses:,.2f}")
        with col3:
            st.metric("🎉 Savings", f"${total_savings:,.2f}", 
                     delta=f"{(total_savings/income*100):.1f}%" if income > 0 else "0%")
        with col4:
            st.metric("💳 Debt", f"${debt:,.2f}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if total_expenses > 0:
                st.plotly_chart(
                    create_pie_chart(current_data['expenses'], "Expense Breakdown"),
                    use_container_width=True
                )
        
        with col2:
            st.plotly_chart(
                create_bar_chart(current_data['expenses'], income, "Budget Overview"),
                use_container_width=True
            )
        
        st.markdown("---")
        st.subheader("📋 Detailed Breakdown")
        expense_df = pd.DataFrame(
            [(cat, f"${amt:,.2f}", f"{(amt/total_expenses*100):.1f}%" if total_expenses > 0 else "0%") 
             for cat, amt in current_data['expenses'].items() if amt > 0],
            columns=['Category', 'Amount', '% of Total']
        )
        expense_df = expense_df.sort_values('Amount', ascending=False)
        st.dataframe(expense_df, use_container_width=True, hide_index=True)
    
    # TAB 3: Trends & Insights
    with tab3:
        st.header("📈 Historical Trends & Insights")
        
        if len(st.session_state.data) > 1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    create_trend_chart(st.session_state.data, 'savings'),
                    use_container_width=True
                )
            
            with col2:
                st.plotly_chart(
                    create_trend_chart(st.session_state.data, 'expenses'),
                    use_container_width=True
                )
            
            st.plotly_chart(
                create_trend_chart(st.session_state.data, 'debt'),
                use_container_width=True
            )
            
            st.markdown("---")
            st.subheader("🧠 Smart Insights")
            insights = calculate_insights(current_data, st.session_state.data)
            
            for insight in insights:
                st.info(insight)
            
            st.markdown("---")
            st.subheader("📊 Month-by-Month Comparison")
            comparison_data = []
            for month, data in sorted(st.session_state.data.items(), reverse=True):
                month_income = data.get('income', 0)
                month_expenses = sum(data.get('expenses', {}).values())
                month_savings = month_income - month_expenses
                month_debt = data.get('debt', 0)
                
                comparison_data.append({
                    'Month': month,
                    'Income': f"${month_income:,.2f}",
                    'Expenses': f"${month_expenses:,.2f}",
                    'Savings': f"${month_savings:,.2f}",
                    'Savings %': f"{(month_savings/month_income*100):.1f}%" if month_income > 0 else "0%",
                    'Debt': f"${month_debt:,.2f}"
                })
            
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)
            
        else:
            st.info("📝 Enter data for at least 2 months to see trends and insights!")
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Tips")
    st.sidebar.markdown("""
    - Save your data regularly
    - Aim for 20% savings rate
    - Track expenses daily
    - Review trends monthly
    """)
    
    # Export functionality
    st.sidebar.markdown("---")
    if st.sidebar.button("📥 Export My Data"):
        export_data = json.dumps(st.session_state.data, indent=2)
        st.sidebar.download_button(
            label="Download JSON",
            data=export_data,
            file_name=f"budget_data_{st.session_state.username}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
