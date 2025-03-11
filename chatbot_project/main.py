import nltk
from chatbot import Chatbot
from summarizer import Summarizer

def download_nltk_resources():
    try:
        # Download both punkt and punkt_tab
        nltk.download('punkt')                             # helps in splitting text into sentences or words.
        # nltk.download('punkt_tab')
        nltk.download('averaged_perceptron_tagger')        # Downloads the averaged_perceptron_tagger, which helps in part-of-speech tagging.
        print("NLTK resources downloaded successfully")
    except Exception as e:
        print(f"Error downloading NLTK resources: {e}")

def main():
    download_nltk_resources()
    bot = Chatbot()                                        # the chatbot is ready to use.
    summarizer = Summarizer()                              # summarizer tool is ready to use.
    print(bot.greet())

    while True:
        user_input = input("You: ").strip()                # strip - unneccessary space will be removed
        if user_input.lower() == "exit":
            print("Sayonara!👋")
            break

        response = bot.respond(user_input)
        print(f"{bot.name}: {response}")

        if "summarize video" in user_input:
            video_url = input("Enter video URL: ")
            summary = summarizer.summarize_video(video_url)
            print(f"{bot.name}: {summary}")
        elif "summarize file" in user_input:
            file_path = input("Enter file path: ")
            summary = summarizer.summarize_file(file_path)
            print(f"{bot.name}: {summary}")

if __name__ == "__main__":
    main()