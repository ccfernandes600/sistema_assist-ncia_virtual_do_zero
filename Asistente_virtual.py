# Importar as bibliotecas necessárias
import speech_recognition as sr
from gtts import gTTS
import os
import wikipediaapi
import webbrowser
import googlemaps
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play

# Função de Text-to-Speech (TTS)
def text_to_speech(text):
    tts = gTTS(text=text, lang='pt')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")

# Função de Speech-to-Text (STT)
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo: ")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='pt-BR')
        print("Você disse: " + text)
        return text
    except sr.UnknownValueError:
        print("Não consegui entender o áudio")
    except sr.RequestError:
        print("Não consegui acessar o serviço de reconhecimento de fala")

# Função para pesquisar no Wikipedia
def search_wikipedia(query):
    wiki_wiki = wikipediaapi.Wikipedia('pt')
    page = wiki_wiki.page(query)
    if page.exists():
        text_to_speech(page.summary)
    else:
        text_to_speech("Não encontrei resultados para a pesquisa.")

# Função para abrir o YouTube
def open_youtube():
    webbrowser.open("https://www.youtube.com")

# Função para localizar a farmácia mais próxima
def find_nearest_pharmacy(api_key):
    gmaps = googlemaps.Client(key=api_key)
    location = gmaps.geolocate()['location']
    places_result = gmaps.places_nearby(location, radius=5000, type='pharmacy')
    if places_result['results']:
        nearest_pharmacy = places_result['results'][0]
        text_to_speech(f"A farmácia mais próxima é {nearest_pharmacy['name']} localizada em {nearest_pharmacy['vicinity']}.")
    else:
        text_to_speech("Não encontrei farmácias próximas.")

# Função principal
def main(api_key):
    while True:
        command = speech_to_text()
        if "Wikipedia" in command:
            text_to_speech("Qual termo você gostaria de pesquisar na Wikipedia?")
            query = speech_to_text()
            search_wikipedia(query)
        elif "YouTube" in command:
            open_youtube()
        elif "farmácia" in command:
            find_nearest_pharmacy(api_key)
        elif "sair" in command:
            text_to_speech("Encerrando o assistente. Até logo!")
            break

# Substitua 'SUA_CHAVE_DE_API_DO_GOOGLE_MAPS' pela sua chave de API do Google Maps
main('SUA_CHAVE_DE_API_DO_GOOGLE_MAPS')
