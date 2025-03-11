import random
import requests

class Chatbot:
    def __init__(self):
        self.name = "Pika"
        self.jokes = [
            "Why don't programmers like nature? It has too many bugs!",
            "Why do Java developers wear glasses? Because they can't C#!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
        ]
        self.facts = [
            "Did you know? The first computer virus was created in 1986 and called Brain!",
            "A single Google query uses more computing power than the entire Apollo 11 moon landing mission!",
            "The first-ever programmer was a woman, Ada Lovelace!"
        ]
        
    def greet(self):
        return f"Hi! I'm {self.name}. I can assist you with\n1. Summarizing video\n2. Summarizing file\n3. Telling joke and fact and weather update.\n4. Type 'exit' to end the conversation.\nHow can I help you today?"

    def get_weather(self, city):
        api_key = "a7181b7f5d198738fe050872c8259471"  
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:                                                  # The API response contains a "cod" key, which is equal to 200 if the request is successful.
                weather = data["weather"][0]["description"].capitalize()
                temp = data["main"]["temp"]
                return f"The weather in {city} is {weather} with a temperature of {temp}°C."
            else:
                return "Sorry, I couldn't find the weather for that city. Please try again."
        except Exception as e:
            return f"Error fetching weather: {str(e)}"
    
    def respond(self, user_input):
        user_input = user_input.lower()
        if "summarize video" in user_input:
            return "Please provide a video link."
        elif "summarize file" in user_input:
            return "Please provide the file path."
        elif "joke" in user_input:
            return random.choice(self.jokes)
        elif "fact" in user_input:
            return random.choice(self.facts)
        elif "weather" in user_input:
            city = input("Enter city name: ")
            return self.get_weather(city)
        elif "hello" in user_input or "hi" in user_input:
            return f"Hello! I'm {self.name}. Need help summarizing something? Or maybe a joke? 😃"
        elif "how are you" in user_input:
            return "I'm just a bot, but I'm feeling great! How about you? 😊"
        elif "thank you" or "thanks" in user_input:
            return "You're welcome! 😊"
        else:
            return "Hey!!! I can summarize videos or files. Try asking me to do that!"

if __name__ == "__main__":
    bot = Chatbot()
    print(bot.greet())
    while True:
        message = input("You: ")
        if message.lower() == "exit":
            print("Sayonara!👋")
            break
        print(f"{bot.name}: {bot.respond(message)}")