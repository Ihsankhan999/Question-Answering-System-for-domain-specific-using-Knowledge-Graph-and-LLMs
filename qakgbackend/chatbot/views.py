from django.http import JsonResponse
from rest_framework.decorators import api_view
import re
from neo4j import GraphDatabase
import google.generativeai as palm

# Initialize Neo4j driver
driver = GraphDatabase.driver("bolt://localhost:7687")

# Configure Google PaLM API
palm.configure(api_key="AIzaSyDX3xa7AfD0Hfru0Zo42I0HfMNOKyZ0T5w")

@api_view(['POST'])
def get_question(request, history=[]):
    if request.method == 'POST':
        question = request.data.get('question')
        print("Question:", question)
        output = generate_and_exec_cypher(question)
        print("Answer", output)
        history.append((question, output))
        return JsonResponse({'question': question, 'answer': [output]})  # Return the answer as an array
    else:
        return JsonResponse({'error': 'Only POST requests are allowed!'}, status=400)


def get_answer(input):
    defaults = {
        'model': 'models/text-bison-001',
        'temperature': 0.7,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
        'max_output_tokens': 1024,
        'stop_sequences': [],
        'safety_settings': [
            {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 1},
            {"category": "HARM_CATEGORY_TOXICITY", "threshold": 1},
            {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 2},
            {"category": "HARM_CATEGORY_SEXUAL", "threshold": 2},
            {"category": "HARM_CATEGORY_MEDICAL", "threshold": 2},
            {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 2}
        ],
    }

    prompt = f"""
    You are an expert in converting English questions to Neo4j Cypher Graph code! The Graph has the following Node Labels: Author, Institute, Major, Paper, Keyword, PublicationVenue, and the following relationships: RELATIONSHIP_TYPE, AUTHORED, ASSOCIATED_WITH, publishIn, AssociatedWith.

    For example,
  

    Example 7 - Who is the author of the paper titled "<PAPER_TITLE>"?
    
    MATCH (a:Author)-[r:RELATIONSHIP]->(p:Paper {{Title: "<PAPER_TITLE>"}})
    RETURN a.Author_Name

    Example 2 - How many papers has "<Author_Name>" published in the field of "<Keyword_Name>"?
    MATCH (a:Author {{Author_Name: "<Author_Name>"}})-[:AUTHORED]->(p:Paper)-[:AssociatedWith]->(k:Keyword {{Keyword_Name: "<Keyword_Name>"}})
    RETURN COUNT(p)
    
    Example 3 - Can you provide a list of papers authored by "<Author_Name>" in "<Keyword_Name>"?
    MATCH (a:Author {{Author_Name: "<Author_Name>"}})-[:AUTHORED]->(p:Paper)-[:AssociatedWith]->(k:Keyword {{Keyword_Name: "<Keyword_Name>"}})
    RETURN p.Title
    
    Example 4 - Which direction does "<Author_Name>" research primarily focus on in "<Keyword_Name>"?
    MATCH (a:Author {{Author_Name: "<Author_Name>"}})-[:AUTHORED]->(p:Paper)-[:AssociatedWith]->(k:Keyword)
    RETURN k.Keyword_Name, COUNT(p) AS PaperCount
    ORDER BY PaperCount DESC

    {input}"""
    
    response = palm.generate_text(**defaults, prompt=prompt)
    return response.result

def extract_query_and_return_key(input_query_result):
    cleaned_query = re.sub(r'[ \n]+', ' ', input_query_result.strip())
    ret_match = re.search(r'RETURN\s+(.*)', cleaned_query)
    return_key = ret_match.group(1).strip() if ret_match else None
    return cleaned_query, return_key

def format_names_with_ampersand(names):
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " & " + names[-1]

def run_cypher_on_neo4j(inp_query, inp_key):
    out_list = []
    with driver.session() as session:
        result = session.run(inp_query)
        for record in result:
            out_list.append(str(record[inp_key]))  # Ensure all outputs are strings
    return format_names_with_ampersand(out_list) if out_list else "No results found."

def generate_and_exec_cypher(input_query):
    generated_query, return_key = extract_query_and_return_key(get_answer(input_query))
    if return_key:
        return run_cypher_on_neo4j(generated_query, return_key)
    return "Invalid query generated."
