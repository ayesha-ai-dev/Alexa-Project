import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLaibrary
import requests
from groq import Groq



recognizer = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    
def aiprocess(command):
    client = Groq(api_key="enter your groq api key here")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",

        messages=[
            {"role": "system", "content": "You are a virtual assistant named Alexa skilled in general tasks."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content
    
    
newsapi_key = "enter your newsapi key here"    
    
def process_command(command):
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif "open chrome" in command:
        webbrowser.open("https://www.google.com/chrome/")
        speak("Opening Chrome")
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
        speak("Opening Facebook")
    elif "open linkedin" in command:
        webbrowser.open("https://www.linkedin.com")
        speak("Opening LinkedIn")  
        
    elif command.lower().startswith("play"):
        song = command.lower().replace("play ", "").strip()
        if song in musicLaibrary.music:
            webbrowser.open(musicLaibrary.music[song])
            speak(f"Playing {song}")
        elif song:
            import yt_dlp
            ydl_opts = {'quiet': True, 'skip_download': True, 'default_search': 'ytsearch1'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song, download=False)
                link = info['entries'][0]['webpage_url']
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak("Please tell me the song name")
        
    elif "news" in command:
        speak("news")
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            if articles:
                for article in articles[:5]:
                    print(article['title'])
                    speak(article['title'])
            else:
                speak("No news articles found.")
        else:
            speak("Sorry, I couldn't fetch the news at the moment.")
    else:
        output = aiprocess(command)
        speak(output)
    
    
        
    
if __name__ == "__main__":
    speak("Initializing Alexa")
    while True:
        print("Listening...")
        
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, phrase_time_limit=5, timeout=5)
                command = recognizer.recognize_google(audio)
                command = command.lower()
                print(command)

                if "alexa" in command:
                    speak("Ya")
                    with sr.Microphone() as source:
                        print("Alexa Active...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        command = command.lower()
                        print(f"You said: '{command}'")  
                        process_command(command)

        except sr.WaitTimeoutError:
            print("Timeout, Listening again...")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")