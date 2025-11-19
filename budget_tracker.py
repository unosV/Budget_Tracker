import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Smart Budget Tracker", 
    page_icon="💰", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS - Just clean background, everything else is default
st.markdown("""
<style>
    .stApp {
        background: #f5f5f5;
    }
    .main .block-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Data file path
DATA_FILE = Path("budget_data.json")

# Default expense categories
DEFAULT_CATEGORIES = [
    "Rent/Mortgage", "Utilities", "Groceries", "Transport", 
    "Entertainment", "Healthcare", "Insurance", "Savings",
    "Debt Repayment", "Dining Out", "Shopping", "Other"
]

def load_data():
    """Load budget data from JSON file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    """Save budget data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_month_key():
    """Get current month key in YYYY-MM format"""
    return datetime.now().strftime("%Y-%m")

def initialize_session_state():
    """Initialize session state variables"""
    if 'data' not in st.session_state:
        st.session_state.data = load_data()
    if 'current_month' not in st.session_state:
        st.session_state.current_month = get_month_key()

def create_pie_chart(expenses_data, title):
    """Create expense breakdown pie chart"""
    df = pd.DataFrame(list(expenses_data.items()), columns=['Category', 'Amount'])
    df = df[df['Amount'] > 0]  # Filter out zero values
    
    # Professional color palette - muted and clean
    colors = ['#3182ce', '#38a169', '#e53e3e', '#d69e2e', '#805ad5', 
              '#dd6b20', '#319795', '#e53e8e', '#2c7a7b', '#c53030',
              '#5a67d8', '#2d3748']
    
    fig = px.pie(df, values='Amount', names='Category', title=title,
                 hole=0.35, color_discrete_sequence=colors)
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        textfont_size=11,
        marker=dict(line=dict(color='white', width=2))
    )
    fig.update_layout(
        height=400,
        title_font_size=18,
        title_font_color='#2d3748',
        font=dict(size=12, color='#2d3748'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        margin=dict(l=20, r=180, t=60, b=20)
    )
    return fig

def create_bar_chart(expenses_data, income, title):
    """Create income vs expenses bar chart"""
    total_expenses = sum(expenses_data.values())
    savings = income - total_expenses
    
    fig = go.Figure(data=[
        go.Bar(
            name='Income', 
            x=['Budget'], 
            y=[income], 
            marker_color='#38a169',
            text=[f'${income:,.0f}'],
            textposition='outside',
            textfont=dict(size=13, color='#2d3748', weight='bold')
        ),
        go.Bar(
            name='Expenses', 
            x=['Budget'], 
            y=[total_expenses], 
            marker_color='#e53e3e',
            text=[f'${total_expenses:,.0f}'],
            textposition='outside',
            textfont=dict(size=13, color='#2d3748', weight='bold')
        ),
        go.Bar(
            name='Savings', 
            x=['Budget'], 
            y=[savings], 
            marker_color='#3182ce',
            text=[f'${savings:,.0f}'],
            textposition='outside',
            textfont=dict(size=13, color='#2d3748', weight='bold')
        )
    ])
    
    fig.update_layout(
        title=title,
        title_font_size=18,
        title_font_color='#2d3748',
        barmode='group',
        height=400,
        yaxis_title='Amount ($)',
        font=dict(size=12, color='#2d3748'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='#e2e8f0', showgrid=True),
        xaxis=dict(showgrid=False),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=60, t=80, b=80)
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
    
    # Professional color scheme based on metric
    colors = {
        'savings': '#38a169',
        'expenses': '#e53e3e',
        'debt': '#d69e2e'
    }
    
    fill_colors = {
        'savings': 'rgba(56, 161, 105, 0.08)',
        'expenses': 'rgba(229, 62, 62, 0.08)',
        'debt': 'rgba(214, 158, 46, 0.08)'
    }
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, 
        y=values, 
        mode='lines+markers',
        name=metric.capitalize(),
        line=dict(width=3, color=colors.get(metric, '#3182ce')),
        marker=dict(size=8, color=colors.get(metric, '#3182ce'), 
                   line=dict(width=2, color='white')),
        fill='tozeroy',
        fillcolor=fill_colors.get(metric, 'rgba(49, 130, 206, 0.08)')
    ))
    
    fig.update_layout(
        title=f"Month-over-Month {metric.capitalize()} Trend",
        title_font_size=18,
        title_font_color='#2d3748',
        xaxis_title="Month",
        yaxis_title=f"Amount ($)",
        height=400,
        hovermode='x unified',
        font=dict(size=12, color='#2d3748'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#e2e8f0', showgrid=True),
        yaxis=dict(gridcolor='#e2e8f0', showgrid=True),
        margin=dict(l=60, r=60, t=70, b=60)
    )
    return fig

def calculate_insights(current_data, historical_data):
    """Generate smart insights based on spending patterns"""
    insights = []
    
    current_income = current_data.get('income', 0)
    current_expenses = sum(current_data.get('expenses', {}).values())
    current_savings = current_income - current_expenses
    current_debt = current_data.get('debt', 0)
    
    # Savings rate
    if current_income > 0:
        savings_rate = (current_savings / current_income) * 100
        if savings_rate > 20:
            insights.append(f"🎉 Great job! You're saving {savings_rate:.1f}% of your income.")
        elif savings_rate > 10:
            insights.append(f"💪 Good! You're saving {savings_rate:.1f}%. Try to reach 20%.")
        else:
            insights.append(f"⚠️ You're only saving {savings_rate:.1f}%. Aim for at least 10-20%.")
    
    # Expense analysis
    if current_expenses > 0:
        expenses_dict = current_data.get('expenses', {})
        top_expense = max(expenses_dict.items(), key=lambda x: x[1])
        insights.append(f"📊 Your highest expense is {top_expense[0]} at ${top_expense[1]:,.2f}")
    
    # Historical comparison
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
    
    # Debt warning
    if current_debt > 0:
        if current_debt > current_income:
            insights.append(f"🚨 Your debt (${current_debt:,.2f}) exceeds your monthly income. Consider debt consolidation.")
        elif current_savings > 0:
            months_to_clear = current_debt / current_savings
            insights.append(f"💡 At your current savings rate, you can clear your debt in {months_to_clear:.1f} months")
    
    # Budget recommendations
    if current_income > 0:
        recommended_savings = current_income * 0.2
        recommended_expenses = current_income * 0.8
        
        if current_expenses > recommended_expenses:
            insights.append(f"💰 Try to reduce expenses to ${recommended_expenses:,.2f} (80% of income)")
    
    return insights

# Initialize
initialize_session_state()

# Header
st.title("💰 Smart Budget Tracker")
st.markdown("""
<div style='text-align: center; color: #718096; font-size: 1.1rem; margin-bottom: 2rem; font-weight: 500;'>
    Track your finances with beautiful insights and smart analytics
</div>
""", unsafe_allow_html=True)

# Sidebar for month selection
st.sidebar.header("Month Selection")
all_months = sorted(list(st.session_state.data.keys()) + [get_month_key()])
all_months = sorted(list(set(all_months)), reverse=True)

selected_month = st.sidebar.selectbox(
    "Select Month",
    all_months,
    index=0 if get_month_key() in all_months else len(all_months)-1
)

st.session_state.current_month = selected_month

# Check if this is a new month
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
    if st.button("💾 Save Month Data", type="primary"):
        save_data(st.session_state.data)
        st.success(f"✅ Data saved for {selected_month}!")

# TAB 2: Current Month Analysis
with tab2:
    st.header(f"Analysis for {selected_month}")
    
    total_expenses = sum(current_data.get('expenses', {}).values())
    total_savings = income - total_expenses
    
    # Key metrics with clean cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💵 Income", f"${income:,.2f}")
    with col2:
        st.metric("💸 Expenses", f"${total_expenses:,.2f}")
    with col3:
        savings_emoji = "🎉" if total_savings > 0 else "⚠️"
        st.metric(f"{savings_emoji} Savings", f"${total_savings:,.2f}", 
                 delta=f"{(total_savings/income*100):.1f}%" if income > 0 else "0%")
    with col4:
        debt_emoji = "💳" if debt > 0 else "✅"
        st.metric(f"{debt_emoji} Debt", f"${debt:,.2f}")
    
    st.markdown("---")
    
    # Charts
    st.subheader("📊 Visual Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        if total_expenses > 0:
            st.plotly_chart(
                create_pie_chart(current_data['expenses'], "Expense Breakdown"),
                width='stretch'
            )
    
    with col2:
        st.plotly_chart(
            create_bar_chart(current_data['expenses'], income, "Budget Overview"),
            width='stretch'
        )
    
    # Detailed breakdown
    st.subheader("📋 Detailed Breakdown")
    expense_df = pd.DataFrame(
        [(cat, amt, f"{(amt/total_expenses*100):.1f}%" if total_expenses > 0 else "0%") 
         for cat, amt in current_data['expenses'].items() if amt > 0],
        columns=['Category', 'Amount', '% of Total']
    )
    expense_df = expense_df.sort_values('Amount', ascending=False)
    st.dataframe(expense_df, width='stretch', hide_index=True)

# TAB 3: Trends & Insights
with tab3:
    st.header("📈 Historical Trends & Insights")
    
    if len(st.session_state.data) > 1:
        # Trend charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                create_trend_chart(st.session_state.data, 'savings'),
                width='stretch'
            )
        
        with col2:
            st.plotly_chart(
                create_trend_chart(st.session_state.data, 'expenses'),
                width='stretch'
            )
        
        st.plotly_chart(
            create_trend_chart(st.session_state.data, 'debt'),
            width='stretch'
        )
        
        # Insights with beautiful cards
        st.subheader("🧠 Smart Insights")
        insights = calculate_insights(current_data, st.session_state.data)
        st.markdown("---")
        
        for i, insight in enumerate(insights):
            # Color code insights
            if "🎉" in insight or "📉" in insight or "Great" in insight:
                st.success(insight)
            elif "⚠️" in insight or "🚨" in insight:
                st.warning(insight)
            else:
                st.info(insight)
        
        # Historical comparison table
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
        
        st.dataframe(pd.DataFrame(comparison_data), width='stretch', hide_index=True)
        
    else:
        st.info("📝 Enter data for at least 2 months to see trends and insights!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips")
st.sidebar.markdown("""
- Save your data regularly
- Aim for 20% savings rate
- Track expenses daily for accuracy
- Review trends monthly
- Prioritize debt repayment
""")

# Export functionality
st.sidebar.markdown("---")
if st.sidebar.button("📥 Export All Data"):
    export_data = json.dumps(st.session_state.data, indent=2)
    st.sidebar.download_button(
        label="Download JSON",
        data=export_data,
        file_name=f"budget_data_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
