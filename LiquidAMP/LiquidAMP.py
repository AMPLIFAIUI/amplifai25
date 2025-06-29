import numpy
import matplotlib.pyplot
import matplotlib.animation
import ast
import sys
import os
import threading

class SelfModifyingAMP:
    def __init__(self):
        self.version = "1.1"
        self.allow_modification = not getattr(sys, 'frozen', False)
        self.setup_ferrofluid()

    def setup_ferrofluid(self):
        matplotlib.pyplot.style.use('dark_background')
        self.figure, self.axis = matplotlib.pyplot.subplots(figsize=(10, 6))
        self.x_values = numpy.linspace(0, 2 * numpy.pi, 100)
        self.line_object, = self.axis.plot([], [], linewidth=4, color='#00f2fe')
        self.axis.axis('off')

    def hot_reload(self, new_code):
        if not self.allow_modification:
            return "🚫 Cannot modify self in EXE mode."
        try:
            ast.parse(new_code)  # Validate code
            with open(__file__, 'w') as file:
                file.write(new_code)
            return f"♻️ AMP v{self.version} upgraded!"
        except Exception as error:
            return f"❌ Failed: {str(error)}"

    def run_terminal(self):
        print(f"⚡ Liquid AMP v{self.version} — Type !help for commands")
        while True:
            try:
                command = input("AMP> ").strip()
                if command.startswith("!upgrade "):
                    path = command[len("!upgrade "):]
                    if os.path.exists(path):
                        with open(path, 'r') as file:
                            new_code = file.read()
                        print(self.hot_reload(new_code))
                    else:
                        print("❌ File not found.")
                elif command == "!help":
                    print("Commands:\n  !upgrade <file.py> - Load and apply new code\n  !quit - Exit terminal\n  !about - Show info")
                elif command == "!about":
                    print("Liquid AMP — Self-modifying animated visual\nBy You 😎")
                elif command == "!quit":
                    print("👋 Exiting terminal...")
                    break
                else:
                    print("❓ Unknown command. Try !help")
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                break

if __name__ == "__main__":
    amp = SelfModifyingAMP()

    def start_animation():
        def animate(frame):
            y_values = numpy.sin(amp.x_values + frame / 10) * numpy.cos(amp.x_values / 2 + frame / 20)
            amp.line_object.set_data(amp.x_values, y_values)
            return amp.line_object,

        animation = matplotlib.animation.FuncAnimation(
            amp.figure,
            animate,
            frames=200,
            interval=50,
            blit=True
        )
        matplotlib.pyplot.show()

    # Start animation and terminal in parallel
    threading.Thread(target=start_animation, daemon=True).start()
    amp.run_terminal()