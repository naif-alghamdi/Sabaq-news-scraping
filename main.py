import openai
import requests
import re
import os

openai.api_key = "Your_openAI_API_Key"

count = 0

if os.path.exists('output.txt'):
    os.remove('output.txt')

#Ftshing JSON Data From sabic web site 
json_headline = requests.get(
    "https://sabq.org/route-data.json?path=%2Fmoment-by-moment").json()

#News data mining
for item in json_headline['data']['collection']['items']:
    json_stroy = requests.get("https://sabq.org/api/v1/stories-by-slug?slug=" +
                              item['story']['slug']).json()
    
    #brack after retreving first 10 articles
    count = count + 1
    if count == 10:
        break;
    
    for headline in item['item']['headline']:
        # Open the file in append mode
        with open('output.txt', 'a', encoding="utf-8") as f:
            # Write headline to the file
            f.write("Headline: " + re.sub(r"<[^>]+>", "", headline) + "\n")

        for item in json_stroy['story']['cards']:

            with open('output.txt', 'a', encoding="utf-8") as f:
                for story in item['story-elements']:

                    if 'text' in story:
                        f.write("Story: " + re.sub(r"<[^>]+>", "", story['text']) + "\n")
                    else:
                        print('The text key does not exist.')

                f.write("-----------------------end of the story------------------------" + "\n")


#Saving and Summaryzing the Data useing AI

# Read the content of the file
with open('output.txt', 'r', encoding='utf-8') as f:
    content = f.read()

#Chat Comletion
response = openai.chat.completions.create(model="gpt-4o-mini",
    messages = [{f"role": "user", "content": f"Summarize the following text: {content} and put it in HTML code because this will be saved in HTML file later (dont add any other word like [Here’s the summarized text formatted in HTML code: ```html])"}])

# Write the summary to HTML file
with open('summary.html', 'w', encoding='utf-8') as f:
    f.write(str(response.choices[0].message.content))