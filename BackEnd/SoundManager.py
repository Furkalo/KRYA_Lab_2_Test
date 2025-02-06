import pygame

class SoundManager:
    """
    A class to manage sound effects in a game using Pygame's mixer module.

    This class initializes the sound system, loads sound files, and provides
    methods to play specific sound effects.
    """
    def __init__(self):
        """Initialize the sound manager and load sounds."""
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        """Load sound effects from the specified file paths."""
        sound_files = {
            'monster': 'assets/sounds/Small monster.wav',
            'plate': 'assets/sounds/Small monster.wav',
            'bird': 'assets/sounds/Bird sound.mp3',
            'laser': 'assets/sounds/Laser Gun.wav'
        }

        for name, path in sound_files.items():
            try:
                # Load sound and set volume
                sound = pygame.mixer.Sound(path)
                sound.set_volume(0.2)  # Reduce volume for better mixing
                self.sounds[name] = sound
            except pygame.error as e:
                print(f"Error loading sound {path}: {e}")  # Print error if loading fails

    def play_sound(self, name):
        """Play a specific sound effect if it exists."""
        if name in self.sounds:
            self.sounds[name].play()
