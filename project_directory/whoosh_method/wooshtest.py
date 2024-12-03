from whoosh import index
from whoosh.writing import AsyncWriter
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
import os


# Define the schema
schema = Schema(
    chapter_id=ID(stored=True),  # Unique identifier for each chapter (e.g., chapter name or number)
    chapter_title=TEXT(stored=True),  # Title of the chapter
    content=TEXT(stored=True)  # Content of the chapter (the main text)
)

# Create the index directory if it doesn't exist
if not os.path.exists("index"):
    os.mkdir("index")

# Create the index object (or open it if it already exists)
ix = index.create_in("index", schema)  # Create a new index in the 'index' directory

# Function to index a single chapter
def index_chapter(file_path, chapter_id, chapter_title, ix):
    # Open the index in writing mode
    writer = ix.writer()

    # Read the content of the chapter from the text file
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()

    # Add the chapter data to the index
    writer.add_document(
        chapter_id=chapter_id,
        chapter_title=chapter_title,
        content=content
    )

    # Commit changes to the index
    writer.commit()

# Directory containing the chapter text files
textbook_dir = r"C:\coding\projects\Pathology finder\TesseractText"

# Index each chapter in the directory
for filename in os.listdir(textbook_dir):
    if filename.endswith(".txt"):
        chapter_id = filename[:-4]  # Assuming filename without '.txt' is the chapter ID
        chapter_title = chapter_id.replace("_", " ").title()  # Example: "chapter_1" becomes "Chapter 1"
        file_path = os.path.join(textbook_dir, filename)

        index_chapter(file_path, chapter_id, chapter_title, ix)
