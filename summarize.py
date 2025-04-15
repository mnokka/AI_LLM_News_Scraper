# Summarices web site (for example english news) and produces own web page for showinfg the summarized data
#
# LLM (Local) open model used in Lenovo ThinkCentre M710q(Intel Core i5-7400T,4 cores, 25Gb mem,NO GPUs )
# 
# Inspired by Udemy course: LLM Engineering: Master AI, Large Language Models & Agents
#
#
# V1.0  15.4.2025   mika.nokka1@gmail.com
#
#
# installations required (linux) : 
# 1) ollama: curl -fsSL https://ollama.com/install.sh | sh
# 2) model:  ollama run llama3.2:1b

import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI


webpage="https://www.helsinkitimes.fi/"
usedmodel="llama3.2:1b" # small and quick model for this purpose, no GPU needs
#usedmodel="llama2:13b" # slow, needs ~25G memory and then swaps to use another 25G


# connect local open "weak machine" ollama model
openai = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Some websites need you to use proper headers when fetching them:
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in normal text. Use capital letters for titles. Do not ask your questions. Do not \
make own comments"


#######################################################################################################
class Website:

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser') # use scraping library
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)
        print(f"Souping done")

        


def user_prompt_for(website):
    return f"Summarize the following content from the website {website.url}:\n\n{website.text}"


def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]


def summarize(url):
    print(f"Starting summarizing prosedure")
    website = Website(url)
    print(f"Starting summarizing creation")
    response = openai.chat.completions.create(
        model = usedmodel,
        messages = messages_for(website)
    )
    return response.choices[0].message.content

def display_summary(url):
    summary = summarize(url)
    print(f"Webpage {webpage} summarized:\n\n")
    print(summary)

###################################################################################
if __name__ == "__main__":
    display_summary(webpage)
