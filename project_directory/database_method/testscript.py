from RiskFactorMapping import risk_factors_mapping
from SymptomFactorMapping import symptoms_mapping

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

user_input = "Chest pain"

print(fuzz.ratio(user_input, "Chest pain"))

user_symptoms = []
response = input(f"Enter your symptoms separated by a comma: ").strip().lower()

# Split the response into a list of symptoms using a comma as the delimiter
user_symptoms = response.split(",")  # This splits at each comma and creates a list

# Strip any extra spaces from each symptom in the list
user_symptoms = [symptom.strip() for symptom in user_symptoms]

# Print the list of symptoms
print(user_symptoms)


#Test should take the user input and compare it against the sympytoms and risk factors for each symptom. 
#If symptoms and factors match, this connection should be stored. later, the program should output the most likely disease and output a recommendation.
for symptom in user_symptoms:
    for key in symptoms_mapping.items():
        for lock in key:
            for pick in lock:
                if fuzz.ratio(pick, symptom)>80: 
                    print(key[0])

matching_keys = [key for key in symptoms_mapping.items() if key == user_input]

# Print the results
print(f"Keys corresponding to '{user_input}': {matching_keys}")

print(symptoms_mapping[next(iter(symptoms_mapping))][1])

