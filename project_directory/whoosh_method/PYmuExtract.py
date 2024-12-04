import fitz
import pymupdf
from fuzzywuzzy import fuzz
from pathlib import Path
import enchant

#This script extracts the pdf into text with a straightforward pymupdf script. However, the library seems to miss a certain font version of f. 
#additionally, the documnet itself missed the letter L for some reason. Becuase of this, some post processing on the document needs to be used. 
#The rest of the script will be processing the text document to match up to 3 words against a single word using a fuzzy search library. 
#i.e. for all words -> fuzzy("ala el", word) -> bestmatch = falafel 
#If the above method causes errors, it is expected to be much less than the original data. 


def main():
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    pdf_path = parent_dir / "Cardiology Textbook.pdf"   

    text = PyMu_Extract(str(pdf_path))
    splitText, splitTerms = split_text(text, current_dir)

    print(fuzz.ratio("oer", "otter"))


def check_words(word1, word2):
    

def PyMu_Extract(Path):
    doc = pymupdf.open(Path) # open a document
    out = open("output.txt", "wb") # create a text output

    text = doc[14].get_text().encode("utf8") # get plain text (is in UTF-8)
    out.write(text)
    out.close()

    print("text extracted")
    return text

def process_terms(terms):
    processedTerms = []
    for i in range(len(terms)-1):
        wordF = False
        for chars in terms[i]:
            if chars == "f" or chars=="F":
                wordF = True
                break
        if wordF == True:
            processedTerms.append(terms[i])
    print(f"length reduced from {len(terms)} to {len(processedTerms)}")
    return processedTerms


def split_text(text, current_dir):
    splitText = text.split()
    #print(splitText)
    termFile = open(str(current_dir / "MedicalWordList.txt"), "r")
    splitTerms = termFile.read().split()
    splitTerms = process_terms(splitTerms)
    return splitText, splitTerms

def fix_text(splitText, splitTerms):
    for i in range(len(splitText)):
        
        matchfound = False
        
        if i+1 < len(splitText): 
            pair = f"{splitText[i]} {splitText[i+1]}"
            print(pair)
            rollingave = 0
            for j in range(len(splitTerms)):
                closeness = fuzz.ratio(pair, splitTerms[j])
                rollingave = closeness + rollingave
                if closeness>60: 
                    matchfound = True
                    print("Match Found!")
                    splitText[i] = splitTerms[j]
                    del splitText[i+1]
                    break
            print(rollingave/j)
    print("Text fixed")
    return splitText

def output_fixed_file(splitText):
    fixedText = ''.join(splitText)
    fixedFile = open("fixedOutput.txt", "w", encoding="utf-8")
    fixedFile.write(fixedText)
    print("text saved")
    return 

if __name__=="__main__":
    main()





