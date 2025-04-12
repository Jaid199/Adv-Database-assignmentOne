#Adv-Database-assignmentOne
D:\sem 5\Adv database\Assignment 1\code\

# Grocery Market Basket Analysis (Apriori & FP-Growth)

This project implements two popular algorithms in data mining — **Apriori** and **FP-Growth** — to perform market basket analysis on a dataset of grocery transactions.

---

## 📁 Project Structure

---

## 📦 Requirements

- Python 3.x
- No additional external libraries are required (uses only built-in modules).

---

## 📊 Dataset

**File:** `grocery_transactions.csv`

- Each row represents a transaction.
- Items are comma-separated.

---

## ▶️ How to Run

Open a terminal or command prompt, navigate to the project folder:

Run **Apriori algorithm**:

Run **FP-Growth algorithm**:

Each script will:

- Load the dataset
- Process frequent itemsets
- Print a summary of frequent items and timing

---

## 📝 Output Summary

- Time taken to run the algorithm
- Total frequent itemsets discovered
- List of frequent products
- Number of generated association rules

---

## 📌 Notes

- Minimum support: `0.02` (2%)
- Minimum confidence: `0.5` (50%)
- Rule generation may result in `0` rules if confidence threshold isn't met.

---

## 👨‍💻 Author

This project was created as part of **Advanced Database Systems** coursework.
Created by Jaid Ibrahim, s075154

> For academic purposes only.
