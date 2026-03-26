# 🏠 ImmoScraper

End-to-end machine learning pipeline for predicting real estate prices in Austria using scraped marketplace data.

This project covers the full workflow from **data acquisition → preprocessing → feature engineering → database storage → model-ready dataset creation**.

---

## 🚀 Features

* 🔍 Automated web scraping (currently supports disclosed)
* 🧹 Data cleaning & normalization pipeline
* 📊 Advanced feature engineering:

  * price per m²
  * log transformations
  * geospatial features 
  * urban classification
* 🗄️ PostgreSQL integration with structured schema
* ⚙️ Batch processing & duplicate handling

---

## 🧱 Tech Stack

* Python (Requests, BeautifulSoup, Pandas, NumPy, sklearn)
* PostgreSQL
* XML-based configuration for data sources

---

## ⚠️ Current Limitations

* Currently supports:

  * 1 Austrian state at a time
  * 1 data source (configurable)

---

## ⚙️ TODOs

    [x] Create a scraper
    [x] Create a data cleaning pipeline
    [x] Create a feature engineering pipeline
    [x] Create a database
    [x] Create urban classification feature
    [x] Add geospatial features
    [x] Implement log_price model
    [ ] Implement ppm2 model
    [x] Add austria module
    [ ] Add GUI

---

## 🛠️ Setup

### 1. Requirements

* Python 3.x
* PostgreSQL
* Tkinter
* Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 2. Database Setup

Create a `.env` file in `/database`:

```env
DB_HOST=your_host
DB_PORT=your_port
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
```

Then execute the provided SQL script to create the schema:

```bash
psql -U your_user -d your_db -f dbSetup.sql
```

---

### 3. Data Source Configuration

Add the following files to `/data/`:

#### `source1.txt`

```text
https://www.disclosed.com
```

#### `source1-name.txt`

```text
example
```

#### `base-links.xml`

```xml
<links>
    <link category="disclosed">
        <immo category="house">
            <type category="rent">
                <link>https://www.disclosed.com/haus-mieten/</link>
            </type>
            <type category="buy">
                <link>https://www.disclosed.com/haus-kaufen/</link>
            </type>
        </immo>

        <immo category="apartment">
            <type category="rent">
                <link>https://www.disclosed.com/mietwohnungen/</link>
            </type>
            <type category="buy">
                <link>https://www.disclosed.com/eigentumswohnung/</link>
            </type>
        </immo>

        <immo category="projects">
            <type category="project">
                <link>https://www.disclosed.com/neubauprojekte/</link>
            </type>
        </immo>
    </link>
</links>
```

---

## ▶️ Run

Execute the imreg script:

```bash
python imreg.py
```

---

## 🧠 Project Structure

```
.
├── scraper/                # scraping logic
├── datamanipulation/       # cleaning & feature engineering
├── database/               # DB connection & insertion
├── data/                   # source configuration
├── mlModels/               # ML models
├── tests/                  # unit tests
├── userinteraction/        # GUI & user interaction modules
├── imreg.py                # main backend script
```

---

## 📌 Notes

This project focuses on **real-world data challenges**:

* incomplete data
* inconsistent formats
* noisy features

and transforms them into a structured dataset suitable for machine learning.

---
