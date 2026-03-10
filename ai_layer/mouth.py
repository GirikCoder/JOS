import pyttsx3
import threading
import queue

class JarvisMouth:
    def __init__(self):
        # We use a queue and a background thread so pyttsx3 doesn't block the main loop
        self.speech_queue = queue.Queue()
        self.thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.thread.start()

    def _speech_worker(self):
        """Background thread that continuously processes speech requests."""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 185)
        self.engine.setProperty('volume', 1.0)
        
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        elif len(voices) > 0:
            self.engine.setProperty('voice', voices[0].id)
            
        while True:
            text = self.speech_queue.get()
            if text is None:
                break
            
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"[SYSTEM] Error during text-to-speech: {e}")
            finally:
                self.speech_queue.task_done()

    def speak(self, text):
        """Adds text to the speech queue to be spoken asynchronously."""
        print(f">>> [JARVIS]: {text}")
        self.speech_queue.put(text)
        
    def wait_until_done(self):
        """Blocks the main thread until the speech queue is completely empty."""
        self.speech_queue.join()
