from tables import pathologies_table, symptoms_table, risk_factors_table
from SymptomFactorMapping import symptoms_mapping
from RiskFactorMapping import risk_factors_mapping

def prompt_user(symptoms, risk_factors):
    user_symptoms = {}
    user_risk_factors = {}

    print("Answer 'yes' or 'no' for the following symptoms:")
    for symptom in symptoms:
        response = input(f"Do you have {symptom}? ").strip().lower()
        user_symptoms[symptom] = response == "yes"

    print("\nAnswer 'yes' or 'no' for the following risk factors:")
    for risk_factor in risk_factors:
        response = input(f"Do you have {risk_factor}? ").strip().lower()
        user_risk_factors[risk_factor] = response == "yes"

    return user_symptoms, user_risk_factors


def calculate_matches(pathologies, symptoms_mapping, risk_factors_mapping, user_symptoms, user_risk_factors):
    results = []

    for pathology in pathologies:
        pathology_symptoms = symptoms_mapping.get(pathology, [])
        pathology_risk_factors = risk_factors_mapping.get(pathology, [])

        matched_symptoms = sum(user_symptoms.get(symptom, False) for symptom in pathology_symptoms)
        matched_risk_factors = sum(user_risk_factors.get(risk_factor, False) for risk_factor in pathology_risk_factors)

        total_criteria = len(pathology_symptoms) + len(pathology_risk_factors)
        if total_criteria > 0:
            match_percentage = (matched_symptoms + matched_risk_factors) / total_criteria * 100
            results.append((pathology, match_percentage))

    return sorted(results, key=lambda x: x[1], reverse=True)


def main():
    # Prompt user for inputs
    user_symptoms, user_risk_factors = prompt_user(symptoms_table, risk_factors_table)

    # Compare user inputs to mappings
    results = calculate_matches(pathologies_table, symptoms_mapping, risk_factors_mapping, user_symptoms, user_risk_factors)

    # Output results
    print("\nResults:")
    if results and results[0][1] > 50:
        for pathology, match_percentage in results:
            if match_percentage > 50:
                print(f"{pathology}: {match_percentage:.2f}% match")
        print(f"\nMost likely pathology: {results[0][0]}")
    else:
        print("Your symptoms do not strongly align with any specific pathology. Please consult your family doctor.")

if __name__ == "__main__":
    main()

