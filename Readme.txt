#  Vehicle Registrations – Investor Dashboard  

A Streamlit dashboard that visualizes **vehicle registration trends in India** using data from the [Vahan Dashboard](https://vahan.parivahan.gov.in).  
The app focuses on **YoY (Year-over-Year)** and **QoQ (Quarter-over-Quarter)** growth of vehicles across categories (2W/3W/4W) and manufacturers.  


##  Features
-  **Filters** – by date range, category (2W/3W/4W), and manufacturer  
-  **KPIs** – Total registrations, Avg YoY Growth %, Avg QoQ Growth %  
-  **Visualizations**  
  - Line chart showing registration trends over time  
  - Bar chart comparing manufacturer-wise registrations  
-  **Investor-Friendly UI** – clean layout with intuitive filters  

---

##  Data Source
- Source: **[Vahan Dashboard](https://vahan.parivahan.gov.in)** (Government of India)  
- Data Collected:  
  - Vehicle type-wise registrations (2W, 3W, 4W)  
  - Manufacturer-wise registrations  
- Steps Taken:  
  - Data exported into CSV (`registrations.csv`) for easier processing  
  - Pre-processed with Python (pandas) to calculate YoY and QoQ growth  

---

##  Tech Stack
- **Python** – Data processing & dashboard logic  
- **Pandas** – Data wrangling & growth calculations  
- **Streamlit** – Interactive dashboard framework  
- **Plotly Express** – Beautiful visualizations  
- (Optional) **SQL** – For further aggregation if needed  

---

##  Setup Instructions

1. Clone the repo:
   ```
   git clone https://github.com/<your-username>/vehicle-dashboard.git
   cd vehicle-dashboard
   ```
2. Create virtual environment & install dependencies:

    ```
    python -m venv venv
    venv\Scripts\activate   # Windows

    pip install -r requirements.txt
    ```
3. Run the dashboard:

    ```
    python -m streamlit run app.py
    ```

## Folder Structure
```
vehicle-dashboard/
│
├── app.py                # Streamlit dashboard
├── registrations.csv     # Sample dataset
├── requirements.txt      # Python dependencies
├── README.md             # Documentation
└── docs/
    └── dashboard.png     # Screenshot for README
```

## Future Enhancements

- Add SQL-based backend queries

- Automate daily scraping from Vahan portal

- Include state-level breakdown for deeper investor insights