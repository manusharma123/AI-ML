import pyttsx3
import speech_recognition as sr
from rich import print


class SpeechAssistant:


    def text_to_speech(self, text):
        """Convert text to speech"""
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # female (try 0 for male)
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        print(f"Assistant: {text}")
        engine.say(text)
        engine.runAndWait()

    def speech_to_text(self, max_attempts=3):
        """Convert speech to text with retries"""
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 1.2
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        attempt = 0

        while attempt < max_attempts:
            with sr.Microphone() as source:
                print(f"Listening... (Attempt {attempt + 1}/{max_attempts})")

                # Adjust noise
                recognizer.adjust_for_ambient_noise(source, duration=1)

                try:
                    audio = recognizer.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=8
                    )

                    text = recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    return text

                except sr.WaitTimeoutError:
                    print("Listening timed out. No speech detected.")
                    attempt += 1

                except sr.UnknownValueError:
                    attempt += 1
                    if attempt < max_attempts:
                        self.text_to_speech("I couldn't understand you. Please try again.")
                    else:
                        self.text_to_speech("Sorry, I couldn't understand you after multiple attempts.")

                except sr.RequestError as e:
                    print(f"API Error: {e}")
                    self.text_to_speech("Speech service is unavailable.")
                    break

        return None


if __name__ == "__main__":
    assistant = SpeechAssistant()

    while True:
        try:
            choice = input(
                "\nChoose an option:\n"
                "1 → Text-to-Speech\n"
                "2 → Speech-to-Text\n"
                "Type 'exit' to quit\n> "
            ).strip().lower()

            if choice == '1':
                text = input("Enter text: ")
                assistant.text_to_speech(text)

            elif choice == '2':
                assistant.speech_to_text()

            elif choice == 'exit':
                assistant.text_to_speech("Goodbye!")
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please enter 1, 2, or 'exit'.")

        except KeyboardInterrupt:
            print("\nProgram interrupted.")
            assistant.text_to_speech("Goodbye!")
            break
