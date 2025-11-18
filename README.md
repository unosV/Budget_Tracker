# 💰 Smart Budget Tracker

A comprehensive personal finance tracker with dynamic visualizations, monthly tracking, and AI-powered insights.

## Features

### ✨ Core Features
- **Dynamic Charts**: Real-time pie charts, bar graphs, and line graphs
- **Monthly Tracking**: Save and switch between different months
- **Expense Categories**: 12 default categories + add custom ones
- **Smart Insights**: AI-powered recommendations based on your spending patterns
- **Trend Analysis**: Month-over-month comparisons for savings, expenses, and debt
- **Data Persistence**: All data saved locally in JSON format
- **Export/Import**: Download your data for backup

### 📊 Visualizations
1. **Pie Chart**: Expense breakdown by category
2. **Bar Graph**: Income vs Expenses vs Savings comparison
3. **Line Graphs**: Historical trends for:
   - Monthly savings
   - Monthly expenses
   - Outstanding debt

### 🧠 Smart Insights
- Savings rate analysis
- Expense trend comparisons
- Debt repayment timeline estimates
- Budget optimization recommendations
- Top expense category identification

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the app**:
```bash
streamlit run budget_tracker.py
```

3. **Access the app**:
- The app will automatically open in your browser at `http://localhost:8501`
- If it doesn't, manually navigate to that URL

## Usage Guide

### First Time Setup

1. **Budget Input Tab**:
   - Enter your monthly income (after tax)
   - Fill in expenses for each category
   - Add your outstanding debt
   - Click "💾 Save Month Data"

2. **Current Month Tab**:
   - View your income, expenses, savings, and debt metrics
   - Analyze pie chart for expense breakdown
   - Check bar graph for budget overview
   - Review detailed expense breakdown table

3. **Trends & Insights Tab**:
   - View month-over-month trends (available after 2+ months)
   - Read smart insights and recommendations
   - Compare historical data in table format

### Monthly Workflow

1. **Start of New Month**:
   - Select the new month from the sidebar dropdown
   - App automatically creates a blank budget for the new month

2. **During the Month**:
   - Update expenses as they occur
   - Click "Save" after each update
   - Check "Current Month" tab to see real-time impact

3. **End of Month**:
   - Ensure all data is saved
   - Review "Trends & Insights" tab for analysis
   - Plan budget adjustments for next month

### Advanced Features

#### Custom Categories
- Go to "Budget Input" tab
- Scroll to "Add Custom Category"
- Enter category name and amount
- Click "Add Category"

#### Export Data
- Click "📥 Export All Data" in sidebar
- Click "Download JSON" to save backup
- Store safely for record-keeping

#### Import Data (Manual)
- Replace `budget_data.json` with your backup file
- Restart the app

## File Structure

```
budget_tracker.py       # Main application
requirements.txt        # Python dependencies
budget_data.json       # Your budget data (created on first save)
```

## Data Format

The app stores data in JSON format:

```json
{
  "2024-11": {
    "income": 5000,
    "expenses": {
      "Rent/Mortgage": 1500,
      "Groceries": 400,
      ...
    },
    "debt": 2000
  }
}
```

## Tips for Best Results

1. **Be Consistent**: Update expenses daily or weekly
2. **Be Honest**: Accurate data = better insights
3. **Review Monthly**: Check trends at month-end
4. **Set Goals**: Aim for 20% savings rate
5. **Track Everything**: Include small expenses
6. **Backup Regularly**: Export data monthly

## Recommended Savings Goals

- **Emergency Fund**: 3-6 months of expenses
- **Savings Rate**: 20% of income (minimum 10%)
- **Debt-to-Income**: Keep debt below monthly income
- **50/30/20 Rule**: 50% needs, 30% wants, 20% savings

## Troubleshooting

### App won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Data not saving
- Check file permissions in the directory
- Ensure you clicked "💾 Save Month Data" button
- Look for `budget_data.json` in the same folder

### Charts not displaying
- Clear browser cache
- Try a different browser
- Check that expense values are > 0

## Future Enhancements (DIY)

Want to make it even smarter? Here are ideas:

1. **AI Integration**: 
   - Add Claude API for personalized financial advice
   - Implement spending predictions using ML

2. **Automation**:
   - Connect to bank APIs for automatic expense tracking
   - Set up email/SMS alerts for budget limits

3. **Advanced Analytics**:
   - Investment portfolio tracking
   - Tax optimization suggestions
   - Retirement planning calculator

4. **Cloud Sync**:
   - Use Google Sheets API for cloud storage
   - Multi-device access via Firebase

5. **Bill Reminders**:
   - Recurring expense tracking
   - Payment due date notifications

## Privacy & Security

- ✅ All data stored **locally** on your machine
- ✅ No data sent to external servers
- ✅ No account registration required
- ✅ You control your financial data
- ⚠️ Remember to backup `budget_data.json` regularly

## Support

Created for personal use. Customize as needed for your requirements.

## License

Free to use and modify for personal use.

---

**Happy budgeting! 💰📊**
