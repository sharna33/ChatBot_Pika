## Chatbot & Summarizer🤖  
This project implements a chatbot that can summarize text files and videos. It also provides jokes, facts, and information on the weather. The chatbot can help users in basic interaction and perform tasks such as summarizing materials, getting the weather, and entertainment from jokes and fun facts.  

## Features🚀   
**1. Summarizing Videos 🎬**: You may provide it a YouTube video link, and the bot will fetch its transcript and make a summary of that video link.  

**2. Summarizing Files 📑**: The bot can summarize text files (.txt) or PDF files (.pdf).  

**3. Jokes and Fun Facts 😂**: The bot can tell jokes and fun facts related to programming and technology. 

**4. Weather Updates 🌦️**: The bot can provide the weather update of a specified city.   

**5. Basic Chat 🗣️**: The bot can greet you and respond to your basic conversational inputs.

## Prerequisites 🔧 
Ensure you have the following libraries installed:

- **nltk (Natural Language Toolkit)** for text processing.  
- **PyPDF2** for reading PDF files.  
- **sumy** for text summarization.  
- **youtube-transcript-api** for fetching YouTube video transcripts.  
- **requests** for fetching weather data from **OpenWeatherMap API**.

You can install the required libraries using pip:   
`pip install nltk PyPDF2 sumy youtube-transcript-api requests`

## Setup 🛠️  
- **Download NLTK Resources 🌐**: The script will download the necessary NLTK resources (e.g., punkt, averaged_perceptron_tagger) during runtime.

- **API Key for Weather 🌤️**: The Chatbot class fetches weather data using the OpenWeatherMap API. You should replace the api_key variable with your own OpenWeatherMap API key. Sign up for a free key at OpenWeatherMap.

## Usage 📲
1. **Run the program**:   
- In your terminal or command prompt, run the following command:  
`python main.py`  

2. **Interact with the chatbot**:

- Type a message to the chatbot, and it will respond.  
- Type exit to end the conversation.

3. **Commands**:
- Type **"summarize video"** and provide a valid YouTube video URL.
- Type **"summarize file"** and provide a valid file path (.txt or .pdf).
- Type **"joke"** to hear a programming-related joke.
- Type **"fact"** to hear an interesting programming or tech fact.
- Type **"weather"** and provide the name of the city to get the current weather.
- Say **"hello"** or **"hi"** to receive a greeting from the bot.
- Type **"exit"** to quit the chatbot.

## Files Structure 🗂️
- **main.py**: The entry point of the application. It initializes and runs the chatbot and summarizer.
- **chatbot.py**: Contains the Chatbot class, which handles interactions with the user.
- **summarizer.py**: Contains the Summarizer class, which handles the text and video summarization.
- **requirements.txt**: List of dependencies required to run the project.

## License 📄
This project is open source and available under the MIT License.