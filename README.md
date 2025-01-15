# property-scraper
p24 and pp property scraper

# Property Scraper Master

## Project Overview

This project is a **Property Scraper** that collects property listing data from **Property24** and **PrivateProperty**. It automates the process of scraping relevant property details and stores the data in structured CSV files.

---

## Features

- **Automated Scraping** of Property24 and PrivateProperty
- **Structured Data Output** (Price, Location, Address, Erf Size, Date Added)
- **Error Handling** with Retry Mechanism
- **Logging** of all actions and errors
- **CSV Data Storage** (Configurable to Database in future upgrades)

---

## Project Structure

```
Property_Scraper_Master/
├── p24_pp_master_scraper.py        # Master script for scraping
├── Privateproperty_Scraper.py      # Scraper for PrivateProperty
├── Property_24_Page_Scraper.py     # Scraper for Property24
├── .gitignore                      # Specifies files to ignore in Git
└── README.md                       # Project documentation
```

---

##  Getting Started

### 1. **Clone the Repository**

```bash
git clone https://github.com/JoeDimumbi/property-scraper.git
cd property-scraper
```

### 2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

> **Note:** If `requirements.txt` is missing, install manually:

```bash
pip install requests beautifulsoup4
```

### 3. **Run the Scraper**

```bash
python p24_pp_master_scraper.py
```

### 4. **Automate the Script**

- **Windows:** Use **Task Scheduler**
- **Linux/Mac:** Use `cron` jobs

---

## Data Output

- **Property24 Listings:** `property24_listings.csv`
- **PrivateProperty Listings:** `privateproperty_listings.csv`

Each CSV file includes:
- Price
- Location
- Address
- Erf Size
- Link
- Date Added

---

## Future Improvements

-  **Email Notifications** when scraping completes
-  **Database Integration** (SQLite/PostgreSQL)
-  **Cloud Deployment** (AWS Lambda/Heroku)
-  **Data Analytics Dashboard**

---

## Contributing

1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License**.

---

## Contact

**Joe Dimumbi**  
📧 Email: [joedims116@gmail.com](mailto:joedims116@gmail.com)  
🔗 GitHub: [JoeDimumbi](https://github.com/JoeDimumbi)

---

_This project was developed to automate property data collection for analysis and market insights._

