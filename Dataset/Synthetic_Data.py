import pandas as pd
import random
from faker import Faker
import os

# Initialize faker
fake = Faker()

# Number of rows
n_rows = 100000

# Define possible categories
genders = ["Male", "Female", "Other"]
smoker_statuses = ["Never", "Former", "Current"]
surgery_types = ["Orthopedic", "Cardiac", "Neuro", "General", "Other"]
cities = ["Chennai", "Bangalore", "Hyderabad", "Delhi"]
outcomes = ["Full_Recovery", "Complications", "Readmitted"]

# Realistic hospital names mapped by city
hospital_mapping = {
    "Chennai": [
        "Apollo Hospitals, Chennai",
        "Sri Ramachandra Hospital, Chennai",
        "MIOT International, Chennai",
        "Kauvery Hospital, Chennai",
        "Fortis Malar Hospital, Chennai"
    ],
    "Bangalore": [
        "Manipal Hospitals, Bangalore",
        "Fortis Hospital, Bangalore",
        "Narayana Health, Bangalore",
        "Cloudnine Hospital, Bangalore",
        "Aster CMI Hospital, Bangalore"
    ],
    "Hyderabad": [
        "Apollo Hospitals, Hyderabad",
        "Yashoda Hospitals, Hyderabad",
        "KIMS Hospital, Hyderabad",
        "Care Hospitals, Hyderabad",
        "Continental Hospitals, Hyderabad"
    ],
    "Delhi": [
        "AIIMS, New Delhi",
        "Fortis Escorts Heart Institute, Delhi",
        "Max Super Speciality Hospital, Saket",
        "Sir Ganga Ram Hospital, Delhi",
        "Apollo Hospital, New Delhi"
    ]
}

# Function to select hospital based on city
def realistic_hospital(city):
    return random.choice(hospital_mapping.get(city, ["Apollo Hospitals"]))

# Generate synthetic dataset
data = []
for i in range(1, n_rows + 1):
    patient_id = i
    name = fake.name()  # Realistic full name instead of generic ID
    age = random.randint(18, 90)
    gender = random.choice(genders)
    diabetes = random.randint(0, 1)
    hypertension = random.randint(0, 1)
    heart_disease = random.randint(0, 1)
    smoker_status = random.choice(smoker_statuses)
    surgery_type = random.choice(surgery_types)
    surgery_date = fake.date_between(start_date="-2y", end_date="today").isoformat()
    
    # Recovery influenced by age and conditions
    base_recovery = random.randint(5, 30)
    if age > 60: base_recovery += random.randint(10, 30)
    if diabetes: base_recovery += random.randint(5, 20)
    if hypertension: base_recovery += random.randint(5, 15)
    recovery_days = min(base_recovery + random.randint(0, 20), 120)
    
    bmi = round(random.uniform(15, 40), 1)
    city = random.choice(cities)
    hospital = realistic_hospital(city)
    outcome = random.choice(outcomes)
    
    data.append([
        patient_id, name, age, gender, diabetes, hypertension, heart_disease,
        smoker_status, surgery_type, surgery_date, recovery_days, bmi,
        hospital, city, outcome
    ])

# Create DataFrame
columns = [
    "patient_id","name","age","gender","diabetes","hypertension","heart_disease",
    "smoker_status","surgery_type","surgery_date","recovery_days","bmi",
    "hospital","city","outcome"
]
df = pd.DataFrame(data, columns=columns)

# Save to absolute path
output_dir = "E:/Projects/Patient_Recovery_Analysis/Dataset/"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "patient_recovery_data_100k.csv")
df.to_csv(output_file, index=False)

print(f"✅ Synthetic dataset generated: {output_file}")
print(df.head(10))
