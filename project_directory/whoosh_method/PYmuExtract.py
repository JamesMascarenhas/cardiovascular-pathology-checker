import fitz
import pymupdf
from fuzzywuzzy import fuzz
from pathlib import Path
import enchant

#This script extracts the pdf into text with a straightforward pymupdf script. However, the library seems to miss a certain font version of f. 
#additionally, the documnet itself missed the letter L. Becuase of this, some post processing on the document needs to be used. 
#The rest of the script will be processing the text document to match up to 3 words against a single word using a fuzzy search library. 
#i.e. for all words -> fuzzy("ala el", word) -> bestmatch = falafel 
#If the above method causes errors, it is expected to be much less than the original data. 


def main():
    #Store respective directories
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    pdf_path = parent_dir / "Cardiology Textbook.pdf"  
    grrmonday = ["h"]
    print(len(grrmonday))
    text = PyMu_Extract(str(pdf_path))  #Exctracts text to a string using pymu
    splitText, splitTerms = split_text(text, current_dir) #Splits both the text and the medical terms into a list. This could be harmfull as we need to carry over the encoding and paragraph structure
    fix_text(splitText, splitTerms, text)
    print(fuzz.ratio("oer", "otter")) # Test to see the ratio result of oer vs otter to simulate something like oer vs offer


def check_words(word1, word2):
    #This function does not provide enough robustness for each case. It fails when there is any punctuation within the word.
    #It also fails to  
    lang = enchant.Dict("en_US") #Set dictionary language
    falseWords = [] 
    if lang.check(word1) == False:
        falseWords.append(word1)
    if lang.check(word2) == False:
        falseWords.append(word2)
    return falseWords #Returns a list of the stored falseWords. 

def PyMu_Extract(Path):
    doc = pymupdf.open(Path) # open a document
    out = open("output.txt", "wb") # create a text-write output
    text = doc[14].get_text() # get plain text 
    wtext = text.encode("utf8") #Encode text for writing to file. 
    out.write(wtext)
    out.close() #Save un-processed text to file "output.txt"

    print("text extracted")
    return text

def process_terms(terms):
    processedTerms = []
    for i in range(len(terms)-1):
        wordF = False       #Reset flag
        for chars in terms[i]:
            if chars == "f" or chars=="F":
                wordF = True 
                break
        if wordF == True:
            processedTerms.append(terms[i]) #F found in word, add to list. 
    print(f"length reduced from {len(terms)} to {len(processedTerms)}")
    return processedTerms

def split_text(text, current_dir):
    splitText = text.split()
    #print(splitText)
    termFile = open(str(current_dir / "MedicalWordList.txt"), "r")
    splitTerms = termFile.read().split()
    splitTerms = process_terms(splitTerms)
    return splitText, splitTerms

def fix_text(splitText, splitTerms, text):
    #Consider changing this function such that it reads from the raw text string and replaces the words there. 
    #In the above iteration, paragraph structure does not need to be considered. 
    print(text)
    for i in range(len(splitText)):
        matchfound = False
        if i+1 < len(splitText): 
            checked = check_words(splitText[i], splitText[i+1]) #Acquire and join list of non-words 
            if len(checked)>0:
                print(f"pair: {checked}")
                pair = 'f'.join(checked)
                for j in range(len(splitTerms)):
                    closeness = fuzz.ratio(pair, splitTerms[j])
                    if closeness>85: 
                        matchfound = True
                        print(f"Match Found! {pair} replace with {splitTerms[j]}")
                        text = text.replace(text, splitTerms[j])
                        break
    print("Text fixed")
    return text

def output_fixed_file(splitText):
    fixedText = ''.join(splitText)
    fixedFile = open("fixedOutput.txt", "w", encoding="utf-8")
    fixedFile.write(fixedText)
    print("text saved")
    return 

if __name__=="__main__":
    main()





