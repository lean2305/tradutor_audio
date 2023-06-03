import tkinter as tk
import importlib
import subprocess
import speech_recognition as sr
import pyttsx3
from googletrans import Translator

# Função para verificar e instalar pacotes necessários
def check_package_installed(package):
    try:
        importlib.import_module(package)
        print(f"{package} está instalado.")
    except ImportError:
        print(f"{package} não está instalado. Instalando...")
        subprocess.check_call(["pip", "install", package])
        print(f"{package} foi instalado com sucesso.")

# Verificar e instalar pacotes necessários
packages = ["speech_recognition", "pyttsx3", "googletrans==4.0.0-rc1"]

for package in packages:
    check_package_installed(package)

# Inicialização do reconhecedor de fala, do mecanismo de síntese de voz e do tradutor
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()


# Configurações da voz
voices = engine.getProperty('voices')
if len(voices) > 0:
    engine.setProperty('voice', voices[0].id)  # Use a primeira voz da lista
else:
    print("Nenhuma voz encontrada. Usando voz padrão.")

# Configurações de velocidade e volume
engine.setProperty('rate', 150)  # Valor ajustável para controlar a velocidade da fala
engine.setProperty('volume', 0.8)  # Valor ajustável para controlar o volume da fala


# Configurações de velocidade e volume
engine.setProperty('rate', 150)  # Valor ajustável para controlar a velocidade da fala
engine.setProperty('volume', 0.8)  # Valor ajustável para controlar o volume da fala

# Restante do código...

def listen():
    with sr.Microphone() as source:
        print("Diga algo...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="pt-BR")
        return text
    except sr.UnknownValueError:
        print("Não foi possível entender a fala.")
    except sr.RequestError as e:
        print(f"Erro ao conectar-se ao serviço de reconhecimento de fala: {e}")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def translate(text, src_lang, dest_lang):
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

def start_assistant():
    user_input = listen()

    if user_input:
        print(f"Usuário: {user_input}")
        translated_input = translate(user_input, src_lang.get(), dest_lang.get())
        print(f"Traduzido: {translated_input}")
        response = "Você disse: " + translated_input
        print(f"Assistente: {response}")
        speak(response)

# Criação da interface gráfica usando Tkinter
window = tk.Tk()
window.title("Assistente de Aprendizado de Idiomas")

# Labels e comboboxes para escolher as línguas de origem e destino
src_lang_label = tk.Label(window, text="Língua de Origem:")
src_lang_label.pack()
src_lang = tk.StringVar()
src_lang_combobox = tk.OptionMenu(window, src_lang, "pt", "en", "es", "fr", "de")
src_lang_combobox.pack()

dest_lang_label = tk.Label(window, text="Língua de Destino:")
dest_lang_label.pack()
dest_lang = tk.StringVar()
dest_lang_combobox = tk.OptionMenu(window, dest_lang, "en", "pt", "es", "fr", "de")
dest_lang_combobox.pack()

# Botão para iniciar o assistente
start_button = tk.Button(window, text="Iniciar", command=start_assistant)
start_button.pack()

window.mainloop()
