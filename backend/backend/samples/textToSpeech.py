import pygame
import pyttsx3
import time

# Initialize Pygame and pyttsx3
pygame.init()
engine = pyttsx3.init()

# Create a screen for the animation
screen_width, screen_height = 500, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Text to Speech with Animated Face")

# Load images for facial expressions (replace with your images)
neutral_face = pygame.Surface((100, 100))  # Placeholder for neutral face
neutral_face.fill((255, 255, 255))  # White background for face (replace with an actual image)

happy_face = pygame.Surface((100, 100))  # Placeholder for happy face
happy_face.fill((255, 255, 0))  # Yellow background for happy face (replace with an actual image)

# Draw a simple face in the center of the screen
def draw_face(face_surface):
    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(face_surface, (screen_width // 2 - 50, screen_height // 2 - 50))  # Draw face in the center
    pygame.display.update()

# Function to change facial expression based on the speech progress
def animate_face(text, speech_rate=150):
    # Split the text into smaller parts to animate with pauses
    sentences = text.split('.')
    for sentence in sentences:
        if sentence.strip():
            # Display happy face for each sentence (replace with logic to change expressions)
            draw_face(happy_face)
            pygame.time.wait(500)  # Wait a little before speech starts
            
            # Convert the sentence to speech and speak it
            engine.setProperty('rate', speech_rate)  # Set the speed of the speech
            engine.say(sentence.strip())
            engine.runAndWait()
            
            # Reset to neutral face after speaking the sentence
            draw_face(neutral_face)
            pygame.time.wait(200)  # Wait a little before animating again

# Main loop
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Sample text to be spoken and animated
        text = "Hello, I am a text to speech module. I can animate a face while I speak."

        # Animate the face while speaking
        animate_face(text)

        # Stop the pygame window when done
        running = False

    pygame.quit()

if __name__ == "__main__":
    main()
