# Smart Complaint Management System

Multi-language complaint management system with dual portals and 10K dataset.

## Features
- 🔴 Citizen Portal - Submit complaints
- 🔵 Admin Dashboard - View all complaints  
- 🌐 Multi-language support (English/Hindi/Marathi)
- ⚡ Auto-classification with priority system
- 📊 10,000 pre-loaded complaints dataset

## Quick Start

```bash
# Install Flask
pip install flask

# Run application
python app.py

# Open browser
http://localhost:5000
```

## Dataset
- `dataset_10k.csv` - 10,000 sample complaints (for reference/training)
- `new_complaints.csv` - Live complaints from citizens (shown in admin dashboard)

## How It Works
1. Citizens submit complaints via Citizen Portal
2. System auto-classifies and assigns priority
3. Complaints saved to `new_complaints.csv`
4. Admin Dashboard shows only citizen-submitted complaints
5. Sorted by priority (urgent first)

## Priority System
- Priority 1 🔥 - Fire/Medical Emergency
- Priority 2 ⚠️ - Electricity Issue
- Priority 3 📌 - Water/Road Issue
- Priority 4 📋 - Garbage Issue

## Priority System
- Priority 1 🔥 - Fire/Medical Emergency
- Priority 2 ⚠️ - Electricity Issue
- Priority 3 📌 - Water/Road Issue
- Priority 4 📋 - Garbage Issue
