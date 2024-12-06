from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir

import re

def clean_highlight(snippet):
    # Remove HTML tags from the snippet
    return re.sub(r'<.*?>', '', snippet)

# Function to search the index
def search_index(query_str, ix):
    with ix.searcher() as searcher:
        # Use the QueryParser to parse the query
        query = QueryParser("content", ix.schema).parse(query_str)

        # Execute the search
        results = searcher.search(query)

        # Print the results
        for result in results:
            print(f"Chapter ID: {result['chapter_id']}")
            print(f"Chapter Title: {result['chapter_title']}")
            #print(f"Snippet: {result['content'][:500]}...")  # Display the first 200 characters of the content
            #print(f"Snippet: {result.highlights('content')}\n")  # Highlight matches in context
            snippet = clean_highlight(result.highlights('content'))
            print(f"Snippet: {snippet}\n")
            print("-" * 80)

# Example search query
search_query = "Heart"  # Replace with your search term
ix = open_dir("index")  # Open the existing index
search_index(search_query, ix)
