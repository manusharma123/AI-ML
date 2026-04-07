import pyttsx3
import speech_recognition as sr

def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')

    # Set a specific voice (e.g., female voice)
    engine.setProperty('voice', voices[1].id)  # Change index to 0 for male voice

    # Set properties before adding anything to the queue
    engine.setProperty('rate', 170)  # Slower speed for better fluency
    engine.setProperty('volume', 1.0)  # Maximum volume for clarity

    # Speak the text
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak now.")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            text_to_speech("Sorry, could not understand what you said. I will try to listen once again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

if __name__ == "__main__":
    while True:
        try:
            choice = input("Choose an option: (1) Text-to-Speech, (2) Speech-to-Text, (type 'exit' to quit): ")
            if choice == '1':
                text = input("Enter the text you want to convert to speech: ")
                text_to_speech(text)
            elif choice == '2':
                speech_to_text()
            elif choice.lower() == 'exit':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 'exit'.")
        except KeyboardInterrupt:
            print("\nProgram terminated by user. Goodbye!")
            break