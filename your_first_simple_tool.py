import anthropic
import wikipedia
client = anthropic.Anthropic()
def generate_wikipedia_reading_list(research_topic, article_titles):
    wikipedia_articles = []
    for t in article_titles:
        results = wikipedia.search(t)
        try:
            page = wikipedia.page(results[0])
            title = page.title
            url = page.url
            wikipedia_articles.append({"title": title, "url": url})
        except:
            continue
    add_to_research_reading_file(wikipedia_articles, research_topic)

def add_to_research_reading_file(articles, topic):
    with open("output/research_reading.md", "a", encoding="utf-8") as file:
        file.write(f"## {topic} \n")
        for article in articles:
            title = article["title"]
            url = article["url"]
            file.write(f"* [{title}]({url}) \n")
        file.write(f"\n\n")
        
def get_research_help(topic, num_articles=3):
    messages = [{"role": "user", "content": f"Give me {num_articles} article titles for this {topic}"}]
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        system="list of possible Wikipedia articles",
        messages=messages,
        max_tokens=500,
    )
    output_text = response.content[0].text
    lines = output_text.split("\n")
    articles = [
        line.split(". ", 1)[1].strip()  # Extract the title after the number and period
        for line in lines
        if line.strip() and line[0].isdigit()  # Ensure the line starts with a number
    ]
    generate_wikipedia_reading_list(topic,articles)


get_research_help("Pirates Across The World", 7)

get_research_help("History of Hawaii", 3)

get_research_help("are animals conscious?", 3)