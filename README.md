# DATA-201 Group Project

## Project Title
Laptop Price Analysis and Dashboard

## Project Overview
This project was developed as part of the DATA-201 course at San José State University. The goal of this project is to analyze laptop prices based on specifications such as brand, CPU, RAM, storage, GPU, screen size, and final price.

The project includes data cleaning, loading the cleaned dataset into a MySQL database, and creating visualizations using a Plotly Dash dashboard.

---

## Team Members
- Shreya Kaushik
- Faith Deanon
- Anurag Sanadi

---

## Project Structure

```text
datacleaning/       -> Data preprocessing and cleaning notebook
mysql/              -> MySQL database loading and query work
plotly/             -> Plotly Dash visualization dashboard
README.md           -> Project documentation
requirements.txt    -> Python dependencies
.gitignore          -> Excludes virtual environment, checkpoints, and environment files
```

---

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- MySQL
- SQLAlchemy
- MySQL Connector/Python
- Plotly
- Dash
- python-dotenv
- Jupyter Notebook
- VS Code

---

## Installation Process

Clone the repository or download the project folder.

Open the project folder in VS Code.

Install all required Python libraries using:

```bash
pip install -r requirements.txt
```

If `pip` is not recognized, use:

```bash
py -m pip install -r requirements.txt
```

If using a virtual environment, activate it first and then run the installation command.

---

## Environment Variables

Database credentials are stored locally in a `.env` file and are not pushed to GitHub.

Each team member should create their own `.env` file in the project root folder:

```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=laptops_db
```

The `.env` file is ignored using `.gitignore` to avoid exposing sensitive information.

---

## Database Setup

Before running the dashboard, create the MySQL database.

Open MySQL Workbench or MySQL command line and run:

```sql
CREATE DATABASE laptops_db;
```

After creating the database, run the notebook below:

```text
mysql/laptopDB.ipynb
```

This notebook loads the cleaned dataset from:

```text
datacleaning/laptops_cleaned.csv
```

into the MySQL table:

```text
laptops
```

---

## Running the Dashboard

After the MySQL database and `laptops` table are created, run the dashboard from the project root folder:

```bash
py plotly/dashboard.py
```

If `py` does not work, use:

```bash
python plotly/dashboard.py
```

Once the dashboard starts, it will run locally at:

```text
http://127.0.0.1:8050/
```

Copy and paste this URL into your browser to view the Plotly Dash dashboard.

---

## Workflow

1. Load the raw laptop dataset.
2. Clean and preprocess the data.
3. Save the cleaned dataset as `laptops_cleaned.csv`.
4. Create the MySQL database `laptops_db`.
5. Load the cleaned dataset into the MySQL table `laptops`.
6. Query the MySQL database.
7. Display analysis results using a Plotly Dash dashboard.

---

## Notes
- Do not commit `.env` or `.venv` files.
- Each team member should use their own local MySQL credentials.
- The cleaned dataset is loaded into a MySQL table named `laptops`.
- The dashboard runs locally at `http://127.0.0.1:8050/`.