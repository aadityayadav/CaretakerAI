import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to capture speech and convert it to text
def listen_and_convert():
    # Using the default microphone as the source
    with sr.Microphone() as source:
        print("Please say something...")
        
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        
        # Listen to the user's speech
        audio = recognizer.listen(source)
        
        try:
            # Convert the speech into text
            text = recognizer.recognize_google(audio)  # Using Google's free API for recognition
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

# Main loop to continuously listen for speech
def main():
    while True:
        # Capture and convert speech to text
        print("main called")
        text = listen_and_convert()
        
        if text:
            # Do something with the text (e.g., pass it to your TTS module)
            # For demonstration, we'll just print the text.
            print("Converted Text: ", text)
            
        # You can add an exit condition (like saying "stop" to exit the loop)
        if "stop" in text.lower():
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
