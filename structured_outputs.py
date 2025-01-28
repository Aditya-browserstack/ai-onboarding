import anthropic
client = anthropic.Anthropic()
import json
translateTool = [
    {
        "name": "language_translation_tool",
        "description":"Tool to translate a given sentence in Spanish, French, Japanese, and Arabic",
        "input_schema":{
          "type": "object",
          "properties": {
              "translated_outputs": {
                  "type":"array",
                  "items":{
                    "type":"string",
                    "description": "Translated sentence in English, Spanish, French, Japanese and Arabic"
                  }
              }
          },
         "required":["english","spanish","french","japanese","arabic"]
        }
    }
]
def translate(originalPhrase):
    query = f"""
    <text>{originalPhrase}</text>
    Only use the language_translation_tool
    """
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=4096,
        system="You are a language translator",
        messages=[{"role":"user","content":query}],
        tools=translateTool
    )  
    printResponse(response)

def printResponse(response):
    json_classification = None
    for content in response.content:
        if content.type == "tool_use" and content.name == "language_translation_tool":
            json_classification = content.input
            break
    print(json.dumps(json_classification, ensure_ascii=False, indent=2))



translate("how much does this cost")


