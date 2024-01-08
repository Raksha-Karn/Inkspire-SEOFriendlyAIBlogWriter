import time
import os
from dotenv import load_dotenv
import threading
import textwrap
import google.generativeai as genai
from IPython.display import Markdown

import PIL.Image
img = PIL.Image.open('bare.jpg')

stop_loading = False
load_dotenv(".env")
API_KEY = os.getenv("GOOGLE_API_KEY")


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def api_request(mood):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro-vision')

    try:
        response = model.generate_content([f"Write a short, engaging blog post based on this picture which is SEO"
                                           f" friendly and the mood of the blog should be {mood}.", img], stream=True)
        response.resolve()
        to_markdown(response.text)

        return response.text
    except:
        global stop_loading
        stop_loading = True
        return None


def loading_process():
    print("Loading: 🪄 ")
    for _ in range(15):
        time.sleep(1)
        print("✨", end="", flush=True)

        if stop_loading:
            print("\nLoading process stopped due to an error.")
            return


def export_to_markdown(data, filename='blog.md'):
    try:
        with open(filename, 'w') as file:
            file.write(data)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")


def main():
    mood = input("What mood would you like the blog to be shown in? ")
    loading_thread = threading.Thread(target=loading_process)
    try:
        loading_thread.start()
        data = api_request(mood)
        loading_thread.join()
        if data is not None:
            print(f"\n\n{data}")
            export_to_markdown(data)
        else:
            print(f"\nFailed to retrieve data.")

    except Exception as main_error:
        print(f"Main function error: {main_error}")



if __name__ == "__main__":
    main()
