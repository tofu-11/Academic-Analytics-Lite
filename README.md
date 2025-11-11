# Academic-Analytics-Lite

This program imports CSV files of student records from multiple class sections. It analyzes the data and outputs each student’s **final grade**, **letter grade**, **percentile**, and **status**. It can also identify **at-risk students** who are close to or already failing, and visualize grade distributions through histograms.

## Program Requirements
- Python 3.10 or higher
- matplotlib
- csv (standard library)

---

## 👥 Developed By
- **Tio, Jedidiah Jubal V.**  
- **Jimenez, Cris Albert**  
- **Dumadapat, Zachary**  
- **Ernacio, Carlos Miguel**

## 🧪 Tested By
- **Daquis, April**  
- **Del Rosario, John Benjamin**

---

## 🧭 Features

### 📁 Automatic Folder Creation
- Automatically creates a folder in the program directory where the user can place CSV files for analysis.

### 📊 Report & Analysis
- Takes a CSV file and outputs each student’s:
  - Final grade  
  - Letter grade  
  - Percentile  
  - Status (e.g., at-risk, passing)
- Separates at-risk students per section and exports them into a separate CSV file.
- Can plot a histogram for a specific section or the entire dataset.

### 🔍 Compare Sections
- Compares at least two sections from a CSV file and displays them in a **sorted table**.
- The table is ordered in **descending mean final grade**, with the highest-performing section at the top.

### 📈 View Improvements
- Takes **two CSV files** from the same section and computes the **differences** between corresponding student records.
- Example: If student A scored 20 on Quiz 1 in File 1 and 25 in File 2, the output will be **+5.00**.
- Students missing from either file are marked as **‘invalid’**.

### 📤 Export Per Section
- Analyzes each section in a CSV file and exports its **statistical data** into a new CSV file.

---

## 🧩 How to Use

1. **Prepare the folder:**
   - Create a folder named `LMS Files` in the same directory as the program and place your CSV files inside.
   - Alternatively, you can run the program once and exit — it will **automatically create** the folder for you.

   > ⚙️ The folder name can be changed in `config.json`.  
   > If renamed manually, the program won’t detect it and will recreate a default folder named `LMS Files`.

2. **Run the program:**
   ```bash
   python main.py
