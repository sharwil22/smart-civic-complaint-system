import csv
import random
from datetime import datetime, timedelta

# Categories with templates
categories = {
    "Fire Emergency": {
        "priority": 1,
        "templates": [
            "Mere building mein aag lag gayi hai",
            "Fire in my building",
            "Aag lagi hai please help",
            "Building me dhuaan aa raha hai",
            "Fire emergency urgent help needed",
            "Ghar mein aag lagi hai jaldi aao",
            "Fire broke out need immediate help"
        ]
    },
    "Medical Emergency": {
        "priority": 1,
        "templates": [
            "Accident hua hai ambulance chahiye",
            "Medical emergency need help",
            "Patient ko hospital le jana hai",
            "Heart attack hua hai",
            "Injured person needs ambulance",
            "Emergency medical help required",
            "Kisi ko dawakhana le jana hai urgent"
        ]
    },
    "Electricity Issue": {
        "priority": 2,
        "templates": [
            "Bijli nahi aa rahi hai",
            "No power supply since morning",
            "Electricity ka problem hai",
            "Transformer blast ho gaya",
            "Current nahi aa raha 2 din se",
            "Power cut for 3 days",
            "Vidyut supply band hai"
        ]
    },
    "Water Issue": {
        "priority": 3,
        "templates": [
            "Paani nahi aa raha hai",
            "Mazya area madhe pani nahi",
            "Water supply band hai",
            "Tanki mein paani nahi",
            "No water for 3 days",
            "Jal supply ka problem hai",
            "Pani supply 1 week se nahi aayi"
        ]
    },
    "Road Issue": {
        "priority": 3,
        "templates": [
            "Sadak pe bada gadda hai",
            "Big pothole on main road",
            "Rasta kharab ho gaya hai",
            "Road repair needed urgently",
            "Khadda bahut bada hai",
            "Street mein bahut gadde hain",
            "Road condition is very bad"
        ]
    },
    "Garbage Issue": {
        "priority": 4,
        "templates": [
            "Kachra nahi uthaya ja raha",
            "Garbage not collected",
            "Safai nahi ho rahi hai",
            "Waste management problem",
            "Kuda yaha se 1 week se pada hai",
            "Cleaning staff not coming",
            "Garbage pile increasing daily"
        ]
    }
}

# Names
names = [
    "Rahul Sharma", "Priya Deshmukh", "Amit Patil", "Sneha Kulkarni",
    "Vikram Singh", "Anjali Mehta", "Rohan Joshi", "Pooja Reddy",
    "Arjun Nair", "Kavita Iyer", "Sanjay Gupta", "Neha Agarwal",
    "Karan Malhotra", "Divya Rao", "Aditya Verma", "Meera Patel",
    "Suresh Kumar", "Anita Desai", "Rajesh Khanna", "Sunita Yadav"
]

# Locations
locations = [
    "MG Road", "Shivaji Nagar", "Kothrud", "Hadapsar", "FC Road",
    "Baner", "Wakad", "Hinjewadi", "Viman Nagar", "Koregaon Park",
    "Pimpri", "Chinchwad", "Aundh", "Deccan", "Camp Area",
    "Kharadi", "Magarpatta", "Katraj", "Warje", "Karve Nagar"
]

# Status options
statuses = ["Pending", "In Progress", "Resolved"]

print("Generating 10,000 complaints dataset...")

# Generate complaints
complaints = []
start_date = datetime.now() - timedelta(days=365)

for i in range(10000):
    category = random.choice(list(categories.keys()))
    complaint_text = random.choice(categories[category]["templates"])
    
    complaint = {
        "id": i + 1,
        "name": random.choice(names),
        "location": random.choice(locations),
        "complaint": complaint_text,
        "category": category,
        "priority": categories[category]["priority"],
        "status": random.choice(statuses),
        "timestamp": (start_date + timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )).strftime("%Y-%m-%d %H:%M:%S")
    }
    
    complaints.append(complaint)
    
    if (i + 1) % 1000 == 0:
        print(f"Generated {i + 1} complaints...")

# Sort by timestamp
complaints.sort(key=lambda x: x["timestamp"])

# Write to CSV
with open("dataset_10k.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["id", "name", "location", "complaint", "category", "priority", "status", "timestamp"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(complaints)

print("\n✅ Dataset created successfully!")
print(f"📁 File: dataset_10k.csv")
print(f"📊 Total complaints: {len(complaints)}")
print(f"\n📈 Category breakdown:")
for category in categories.keys():
    count = sum(1 for c in complaints if c["category"] == category)
    print(f"   {category}: {count}")
