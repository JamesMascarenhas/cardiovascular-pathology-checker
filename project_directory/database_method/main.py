'''
Importation of all tables used in the script 
'''

from pathologies_info import pathologies_table
from symptoms_info import symptoms_table
from risk_factors_info import risk_factors_table
from pathology_symptom_mapping import symptoms_mapping
from pathology_risk_factor_mapping import risk_factors_mapping

'''
Importing fuzzywuzzy to accomodate for any small typos within the user input
'''
from fuzzywuzzy import fuzz

'''
Function to display both the symptoms and risk facrtors tables to the user so they know what they should input if experiencing them
'''
def display_list(items, title):
    print(f"\nList of Relevant {title}:")
    for item in items:
        print(f"- {item}")

'''
Function asking the user to input their relevant symptoms and risk factors for all cardiovascular pathologies
'''
def get_user_inputs(prompt_message):
    user_inputs = input(f"{prompt_message}").strip().lower()

    # Take into account if user made a mistake or wants to quit the program
    if user_inputs == 'q':
        print("You chose to quit the program")
        quit()
    
    user_inputs_list = [item.strip() for item in user_inputs.split(",") if item.strip()]
    return user_inputs_list

'''
Function to calculate the number of matches between the user input and the symptoms and risk factors for each pathology
Using fuzzy wuzzy in the matching process to address any typos that the user may have had
Determining the percentage of matching symptoms and risk factors the user has to each pathology
Returning a list of all the pathologies with their percentages of overlapping symptoms/risk factors as the user
'''
def calculate_matches(pathologies, symptoms_mapping, risk_factors_mapping, user_symptoms, user_risk_factors):
    results = []

    # Normalize user inputs
    normalized_user_symptoms = [symptom.lower().strip() for symptom in user_symptoms]
    normalized_user_risk_factors = [risk_factor.lower().strip() for risk_factor in user_risk_factors]

    # Iterating through each pathology and loading it's symptoms and risk factors
    for pathology in pathologies: 
        pathology_symptoms = [symptom.lower().strip() for symptom in symptoms_mapping.get(pathology, [])]
        pathology_risk_factors = [risk_factor.lower().strip() for risk_factor in risk_factors_mapping.get(pathology, [])]

        # Match symptoms using fuzzy matching to account for typos
        matched_symptoms = sum(
            any(fuzz.ratio(user_symptom, pathology_symptom) > 80 for pathology_symptom in pathology_symptoms)
            for user_symptom in normalized_user_symptoms
        )

        # Match risk factors using fuzzy matching to account for typos
        matched_risk_factors = sum(
            any(fuzz.ratio(user_risk_factor, pathology_risk_factor) > 80 for pathology_risk_factor in pathology_risk_factors)
            for user_risk_factor in normalized_user_risk_factors
        )

        # Calculate match percentage for each pathology
        total_criteria = len(pathology_symptoms) + len(pathology_risk_factors)
        if total_criteria > 0:
            match_percentage = (matched_symptoms + matched_risk_factors) / total_criteria * 100
            results.append((pathology, match_percentage))

    # Returning a list of tuples each being the pathology and its percentage, sorted from highest percentage to lowest
    return sorted(results, key=lambda x: x[1], reverse=True)


def main():
    '''
    Ask if the user wants to see the list of relevant symptoms then ask what their symptoms are
    '''
    view_symptoms = input("Would you like to see a list of relevant symptoms? (yes/no): ").strip().lower()
    if view_symptoms == "yes":
        display_list(symptoms_table, "Symptoms")
        
    # Prompting the user to enter their relevant symptoms and indicating if they wish to quit to type q
    user_symptoms = get_user_inputs("Enter the relevant symptoms you are experiencing (separated by commas) or if you wish to quit the program type 'q': ")

    '''
    Ask if the user wantes to see the list of relevant risk factors then ask what their risk factors are
    '''
    view_risk_factors = input("Would you like to see a list of relevant risk factors? (yes/no): ").strip().lower()
    if view_risk_factors == "yes":
        display_list(risk_factors_table, "Risk Factors")

    # Prompting the user to enter their relevant risk factors  and indicating if they wish to quit to type q
    user_risk_factors = get_user_inputs("Enter the relevant risk factors that apply to you (separated by commas) or if you wish to quit the program type 'q': ")

    '''
    Compare user inputs to mappings
    '''
    results = calculate_matches(
        pathologies_table.keys(), symptoms_mapping, risk_factors_mapping, user_symptoms, user_risk_factors
    )

    '''
    Output results
    '''
    print("\nResults:")
    
    # If the highest matcher percentage is above 50% then look at each pathology
    if results and results[0][1] > 50:
        for pathology, match_percentage in results:
            if match_percentage > 50:
                print(f"{pathology}: {match_percentage:.2f}% match")
        most_likely_pathology = results[0][0]
        print(f"\nYour most likely pathology is: {most_likely_pathology}")
        print(f"Description: {pathologies_table[most_likely_pathology]}")
        print("Suggestion: You should go to the emergency room as soon as possible")
        
    # Else not of the pathologies overlap enough and a visit to the family doctor is recommended
    else:
        print("Your symptoms do not strongly align with any specific pathology")
        print("Suggestion: However they are still worrisome and you should consult your family doctor")


if __name__ == "__main__":
    main()
