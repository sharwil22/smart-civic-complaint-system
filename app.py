from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Complaint categories with priority levels
CATEGORIES = {
    "Fire Emergency": {
        "priority": 1, 
        "keywords": [
            # English
            "fire", "burning", "smoke", "flames", "blaze", "burn",
            # Hindi
            "aag", "aag lag", "aag lagi", "aag lagayi", "dhuaan", "dhua", "dhuan",
            "jal", "jalaa", "jala raha", "jal raha", "dhuwaan",
            # Marathi
            "aag", "dhuaar", "jalat", "jalt"
        ]
    },
    "Medical Emergency": {
        "priority": 1, 
        "keywords": [
            # English
            "medical", "emergency", "hospital", "ambulance", "accident", "injured",
            "doctor", "patient", "sick", "health", "urgent medical", "critical",
            # Hindi
            "dawakhana", "bimar", "bemar", "hospital", "ambulance", "accident",
            "chot", "ghayal", "doctor", "daktar", "marij", "patient",
            # Marathi
            "hospital", "ambulance", "aajari", "doctor", "daktar"
        ]
    },
    "Electricity Issue": {
        "priority": 2, 
        "keywords": [
            # English
            "electricity", "power", "light", "current", "transformer", "electric",
            "power cut", "no power", "no light", "blackout", "voltage",
            # Hindi
            "bijli", "bijali", "vidyut", "vidut", "current", "light", "transformer",
            "bijli nahi", "bijali nahi", "power nahi", "light nahi",
            # Marathi
            "vij", "vidyut", "light", "current", "bijli"
        ]
    },
    "Water Issue": {
        "priority": 3, 
        "keywords": [
            # English
            "water", "tank", "supply", "tap", "pipeline", "no water", "water supply",
            # Hindi
            "paani", "pani", "jal", "paani nahi", "pani nahi", "pani supply",
            "tanki", "tank", "nal", "paani ka", "pani ka", "jal supply",
            # Marathi
            "pani", "paani", "pani nahi", "paani nahi", "pani nahi ahe",
            "paani nahi ahe", "pani purvatha", "tanki", "nal"
        ]
    },
    "Road Issue": {
        "priority": 3, 
        "keywords": [
            # English
            "road", "pothole", "street", "highway", "path", "road repair",
            "broken road", "damaged road",
            # Hindi
            "sadak", "sadak", "gadda", "gadde", "rasta", "raasta", "khadda", "khaddaa",
            "sadak kharab", "rasta kharab", "sadak toot", "road",
            # Marathi
            "rasta", "raasta", "khadda", "khaddaa", "sadak", "rasta kharab"
        ]
    },
    "Garbage Issue": {
        "priority": 4, 
        "keywords": [
            # English
            "garbage", "waste", "trash", "cleaning", "dustbin", "sanitation",
            "dirty", "clean", "garbage collection",
            # Hindi
            "kachra", "kachara", "kachhra", "kuda", "safai", "saaf", "gandagi",
            "kachra nahi", "safai nahi", "kuda nahi", "kachra uthao",
            # Marathi
            "kachra", "kachara", "safai", "gandagi", "kachra nahi"
        ]
    },
    "Other": {"priority": 5, "keywords": []}
}

DATASET_FILE = "dataset_10k.csv"
NEW_COMPLAINTS_FILE = "new_complaints.csv"

def load_complaints():
    """Load only new complaints submitted by citizens"""
    complaints = []
    
    # Load only new complaints (not the 10K dataset)
    if os.path.exists(NEW_COMPLAINTS_FILE):
        with open(NEW_COMPLAINTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['id'] = int(row['id'])
                row['priority'] = int(row['priority'])
                complaints.append(row)
    
    return complaints

def save_new_complaint(complaint):
    """Save new complaint to CSV file"""
    file_exists = os.path.exists(NEW_COMPLAINTS_FILE)
    
    with open(NEW_COMPLAINTS_FILE, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'name', 'location', 'complaint', 'category', 'priority', 'status', 'timestamp']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(complaint)

def classify_complaint(text):
    """Classify complaint based on keywords"""
    text_lower = text.lower()
    
    for category, data in CATEGORIES.items():
        if category == "Other":
            continue
        for keyword in data["keywords"]:
            if keyword in text_lower:
                return category, data["priority"]
    
    return "Other", CATEGORIES["Other"]["priority"]

@app.route('/')
def home():
    """Home page with portal selection"""
    return render_template('home.html')

@app.route('/citizen')
def citizen_portal():
    """Citizen complaint submission portal"""
    return render_template('citizen.html')

@app.route('/submit', methods=['POST'])
def submit_complaint():
    """Handle complaint submission"""
    name = request.form.get('name', '').strip()
    location = request.form.get('location', '').strip()
    complaint_text = request.form.get('complaint', '').strip()
    
    if not name or not location or not complaint_text:
        return jsonify({'success': False, 'message': 'All fields are required!'})
    
    # Classify complaint
    category, priority = classify_complaint(complaint_text)
    
    # Get next ID (start from 1 for new complaints)
    all_complaints = load_complaints()
    next_id = len(all_complaints) + 1
    
    # Create complaint object
    complaint = {
        "id": next_id,
        "name": name,
        "location": location,
        "complaint": complaint_text,
        "category": category,
        "priority": priority,
        "status": "Pending",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save complaint
    save_new_complaint(complaint)
    
    return jsonify({
        'success': True,
        'complaint': complaint
    })

@app.route('/admin')
def admin_portal():
    """Admin dashboard to view complaints"""
    complaints = load_complaints()
    # Sort by priority (ascending) and then by timestamp
    sorted_complaints = sorted(complaints, key=lambda x: (x['priority'], x['timestamp']))
    return render_template('admin.html', complaints=sorted_complaints)

@app.route('/api/complaints')
def get_complaints():
    """API endpoint to get all complaints"""
    complaints = load_complaints()
    sorted_complaints = sorted(complaints, key=lambda x: (x['priority'], x['timestamp']))
    return jsonify(sorted_complaints)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏛️  SMART COMPLAINT MANAGEMENT SYSTEM")
    print("="*60)
    print("\n🌐 Server starting...")
    print("\n📱 Open in browser:")
    print("   http://localhost:5000")
    print("\n🔴 Citizen Portal: http://localhost:5000/citizen")
    print("🔵 Admin Portal:   http://localhost:5000/admin")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
