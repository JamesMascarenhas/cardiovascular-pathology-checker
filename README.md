# cardiovascular-pathology-checker

## Description
- The purpose of this project is to provide individuals who have cardiovascular symptoms and risk factors with a trustworthy tool for telling
  them what pathologies they may have and what type of care to seek (emergency room or family doctor)
- This project is meant to combat the misinformation of looking up symptoms online which tends to return an overly severe illness and can scare people
- The information for this project is derived from a cardiovascular textbook given to medical students at the University of Ottawa and from the Mayo Clinic
- This project will first be released to medical students as a means of studying, and if successful will be made available to the public

## Set Up
- The First version of this project uses a database of the relevant symptoms and risk factors associated with several different cardiovascular pathologies
  derived from both the cardiovascular pathologies textbook and the Mayo Clinic online
  - This version simply compares the symptoms and risk factors a user inputs to the ones for each pathology and if above a certain threshold will define
      the pathology for the user and make a suggestion of where to get care
  - Still working on how to weigh different symptoms and risk factors as they obviously are not all as strongly associated with specific pathologies
  
- The Second version of this project uses Whoosh and text extraction to create a search engine within the cardiovascular pathologies textbook
    in which it can scan the textbook for similar symptoms and risk factors listed by the user and output back which pathology this is most associated with
  - This aspect of the project leans more toward the side of providing a study diagnostic tool for medical students
  - Tesseract and PyMu are being used to extract text data from the PDF of the textbook
  - Whoosh creates indexes of the different chapters (pathologies) and assesses which has the greatest matching with the user input

- The Third version of this project will incorporate the usage of a large language model (LLM) for retrieval-augmented generation 
  - When completing this version will have to correct for LLM hallucinations especially if this will be used by the public to assess health
