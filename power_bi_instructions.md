# Power BI Dashboard Instructions

This document provides step-by-step instructions to recreate the Customer Churn Prediction & Retention Dashboard in Power BI.

## 1. Data Connection
1. Open Power BI Desktop.
2. Click on **Get Data** -> **Text/CSV**.
3. Navigate to your project folder and select `data/synthetic_churn_data.csv`.
4. Click **Load** (or **Transform Data** if you wish to clean/format columns like rounding Monthly Charges).

## 2. Key Performance Indicators (KPIs)
Create cards for the following metrics:
- **Total Customers**: Add a Card visual. Drag `CustomerID` into the fields and set aggregation to Count (Distinct).
- **Churn Rate**: 
  - Create a Measure: `Churn Rate = CALCULATE(COUNT(data[Churn]), data[Churn]="Yes") / COUNT(data[CustomerID])`
  - Add a Card visual and format the measure as a Percentage.
- **Average Tenure**: Add a Card visual, drag `Tenure`, set aggregation to Average.
- **Average Monthly Revenue**: Add a Card visual, drag `MonthlyCharges`, set aggregation to Average.

## 3. Visualizations
### Churn Distribution (Donut Chart)
- **Visual**: Donut Chart
- **Legend**: `Churn`
- **Values**: Count of `CustomerID`
- **Colors**: Format "Yes" to a prominent color (e.g., Orange/Red) and "No" to a neutral color (e.g., Dark Blue).

### Churn by Contract Type (Clustered Bar Chart)
- **Visual**: Clustered Bar Chart
- **Y-Axis**: `ContractType`
- **X-Axis**: Count of `CustomerID`
- **Legend**: `Churn`

### Monthly Trend Analysis (Line Chart)
*Note: Since the dataset doesn't have an explicit date column, you can simulate a trend by grouping Tenure into buckets (e.g., 0-12 months, 13-24 months) or sorting by Tenure.*
- **Visual**: Line Chart
- **X-Axis**: `Tenure`
- **Y-Axis**: Count of `CustomerID`
- **Legend**: `Churn`

### Customer Segmentation (Tree Map or Matrix)
- **Visual**: Matrix
- **Rows**: `PaymentMethod`
- **Columns**: `ContractType`
- **Values**: Count of `CustomerID`

## 4. Filters & Slicers
Add the following slicers to the left or top panel to allow users to interact with the data:
- `ContractType`
- `Gender`
- `PaymentMethod`

## 5. Styling
- **Theme**: Use a modern dark theme or a clean white SaaS theme. Go to `View` -> `Themes` and select or customize one.
- **Layout**: Keep KPIs at the top, followed by the main charts. Add a title at the very top: "Customer Churn & Retention Analytics".
