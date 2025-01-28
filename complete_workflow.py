import anthropic
import wikipedia
import re

client = anthropic.Anthropic()

article_search_tool = {
    "name": "get_article",
    "description": "A tool to retrieve an up-to-date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a Wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}

def get_article(search_term):
    results = wikipedia.search(search_term)
    if not results:
        return "No relevant wikipedia articles found"
    first_result = results[0]
    page = wikipedia.page(first_result, auto_suggest=False)
    return page.content

def extract_answer_from_tags(response_text):
    match = re.search(r'<answer>(.*?)</answer>', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response_text

def answer_question(question):
    system_prompt = """
    You will be asked a question by the user. 
    If answering the question requires data you were not trained on, you can use the get_article tool to get the contents of a recent Wikipedia article about the topic. 
    If you can answer the question without needing to get more information, please do so. 
    Only call the tool when needed. 
    When you can answer the question, keep your answer as short as possible and enclose it in <answer> tags.
    """
    prompt = f"""
    Answer the following question: <question>{question}</question>
    """
    messages = [{"role": "user", "content": prompt}]

    while True:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            system=system_prompt, 
            messages=messages,
            max_tokens=1000,
            tools=[article_search_tool]
        )
        
        if response.stop_reason == "tool_use":
            tool_use = response.content[-1]
            tool_name = tool_use.name
            tool_input = tool_use.input
            messages.append({"role": "assistant", "content": response.content})

            if tool_name == "get_article":
                search_term = tool_input["search_term"]
                print(f"Claude wants to get an article for: {search_term}")
                wiki_result = get_article(search_term) 
                tool_response = {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": wiki_result
                        }
                    ]
                }
                messages.append(tool_response)

        else:
            final_answer = response.content[0].text
            extracted_answer = extract_answer_from_tags(final_answer)
            print("Claude's final answer:")
            print(extracted_answer)
            break

def chatbot():
    print("Welcome to the Claude Chatbot! Type your questions, and I'll do my best to answer them.")
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye! Thanks for chatting with me.")
            break
        
        print("\nClaude is thinking...")
        answer_question(user_input)
        print()  

chatbot()