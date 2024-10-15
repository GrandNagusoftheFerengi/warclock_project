import tkinter as tk
from tkinter import ttk, messagebox
import time

class WarClock:
    def __init__(self, root):
        """Initialize the WarClock application."""
        self.root = root
        self.root.title("Warhammer 40K WarClock")
        self.root.geometry("800x480")
        self.root.configure(bg='#1e1e1e')  # Dark background

        self.factions = ["Adepta Sororitas", "Adeptus Custodes", "Adeptus Mechanicus", "Aeldari", "Astra Militarum", "Black Templars", "Blood Angels", "Chaos Daemons", "Chaos Knights", "Dark Angels", "Dark Mechanicum", "Death Guard", "Deathwatch", "Drukhari", "Genestealer Cult", "Grey Knights", "Imperial Agents", "Imperial Knights", "Necrons", "Orks", "Space Marines", "Space Wolves", "T'au Empire", "Thousand Sons", "Tyranids", "Votann", "World Eaters"]
        self.game_lengths = [30, 60, 90, 120, 240]  # In minutes

        # Define faction colors
        self.faction_colors = {
            "Adepta Sororitas": "#e6e6fa", #lavender
            "Adeptus Custodes": "#ffd700", #Gold
            "Adeptus Mechanicus": "#8b0000", #Dark Red
            "Aeldari": "#9400d3", #Dark Violet
            "Astra Militarum": "#556b2f", #Dark Olive Green
            "Black Templars": "#000000", #Black
            "Blood Angels": "#ff0000", #Red
            "Chaos Daemons": "#ff4500", #Orange Red
            "Chaos Knights": "#8b4513", #Saddle Brown
            "Dark Angels": "#006400", #Dark Green
            "Dark Mechanicum": "#2f4f4f", #Dark Slate Gray
            "Death Guard": "#556b2f", #Dark Olive Green
            "Deathwatch": "#808080", #Gray
            "Drukhari": "#483d8b", #Dark Slate Blue
            "Genestealer Cult": "#800080", #Purple
            "Grey Knights": "#a9a9a9", #Dark Gray
            "Imperial Agents": "#4682b4", #Steel Blue
            "Imperial Knights": "#b0c4de", #Light Steel Blue
            "Necrons": "#228b22", #Forest Green
            "Orks": "#32cd32", #Lime Green
            "Space Marines": "#0000ff", #Blue
            "Space Wolves": "#4682b4", #Steel Blue
            "T'au Empire": "#ffa500", #Orange
            "Thousand Sons": "#4b0082", #Indigo
            "Tyranids": "#8b008b", #Dark Magenta
            "Votann": "#d2691e", #Chocolate
            "World Eaters": "#b22222" #Firebrick
        }

        # Players info placeholder
        self.players = [{"faction": "", "time": 0, "victory_points": 0, "command_points": 0} for _ in range(2)]

        # Game time placeholder
        self.total_time = 0  # Total game time in seconds
        self.remaining_time = 0  # Remaining time from total game time

        # Start with Game Mode selection screen
        self.create_game_mode_screen()

    def create_game_mode_screen(self):
        """Creates the Game Mode selection screen."""
        self.game_mode_frame = ttk.Frame(self.root, padding="20")
        self.game_mode_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.game_mode_frame, text="Game Mode Start", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        # Game length selection
        ttk.Label(self.game_mode_frame, text="Game Mode (minutes):").grid(row=1, column=0, padx=10, pady=10)
        self.game_length_var = tk.IntVar(value=self.game_lengths[1])
        ttk.Combobox(self.game_mode_frame, textvariable=self.game_length_var, values=self.game_lengths).grid(row=1, column=1, padx=10, pady=10)

        # Start game button
        ttk.Button(self.game_mode_frame, text="Start", command=self.start_game_mode).grid(row=2, column=0, columnspan=2, pady=20)

    def start_game_mode(self):
        """Starts the total game timer and proceeds to faction selection."""
        if not self.game_length_var.get():
            messagebox.showwarning("Incomplete Selection", "Please select a game length.")
            return
        # Set total game time
        self.total_time = self.game_length_var.get() * 60  # Convert minutes to seconds
        self.remaining_time = self.total_time

        # Start the total game timer
        self.start_time = time.perf_counter()
        self.last_update = self.start_time
        self.game_running = True

        # Destroy game mode screen and proceed to faction selection
        self.game_mode_frame.destroy()
        self.create_faction_select_screen()

        # Start updating the total game timer
        self.update_total_time()

    def create_faction_select_screen(self):
        """Creates the faction selection screen with a persistent clock countdown."""
        self.faction_select_frame = ttk.Frame(self.root, padding="20")
        self.faction_select_frame.grid(row=0, column=0, padx=10, pady=10)

        # Persistent clock countdown
        self.total_time_label = ttk.Label(self.faction_select_frame, text="", font=("Arial", 24, "bold"))
        self.total_time_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.update_total_time_display()

        # Increase font size for the title
        ttk.Label(self.faction_select_frame, text="Select Factions", font=("Arial", 28, "bold")).grid(row=1, column=0, columnspan=2, pady=20)

        # Create a style for larger Comboboxes
        style = ttk.Style()
        style.configure('Large.TCombobox', padding=5, font=('Arial', 14))

        # Player 1 setup
        ttk.Label(self.faction_select_frame, text="First Turn Faction:", font=("Arial", 16)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.player1_faction_var = tk.StringVar(value=self.factions[0])
        ttk.Combobox(self.faction_select_frame, textvariable=self.player1_faction_var, values=self.factions, style='Large.TCombobox', width=30).grid(row=2, column=1, padx=10, pady=10)

        # Player 2 setup
        ttk.Label(self.faction_select_frame, text="Final Turn Faction:", font=("Arial", 16)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.player2_faction_var = tk.StringVar(value=self.factions[0])
        ttk.Combobox(self.faction_select_frame, textvariable=self.player2_faction_var, values=self.factions, style='Large.TCombobox', width=30).grid(row=3, column=1, padx=10, pady=10)

        # Create a style for a larger button
        style.configure('Large.TButton', font=('Arial', 16), padding=10)

        # Select button
        ttk.Button(self.faction_select_frame, text="Select", command=self.start_game, style='Large.TButton').grid(row=4, column=0, columnspan=2, pady=20)

    def update_total_time_display(self):
        """Updates the display of the total game timer."""
        if self.game_running:
            current_time = time.perf_counter()
            self.remaining_time = max(0, self.total_time - (current_time - self.start_time))
            minutes, seconds = divmod(int(self.remaining_time), 60)
            self.total_time_label.config(text=f"Time Remaining: {minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_total_time_display)

    def start_game_mode(self):
        """Starts the total game timer and proceeds to faction selection."""
        if not self.game_length_var.get():
            messagebox.showwarning("Incomplete Selection", "Please select a game length.")
            return
        # Set total game time
        self.total_time = self.game_length_var.get() * 60  # Convert minutes to seconds
        self.remaining_time = self.total_time

        # Start the total game timer
        self.start_time = time.perf_counter()
        self.last_update = self.start_time
        self.game_running = True

        # Destroy game mode screen and proceed to faction selection
        self.game_mode_frame.destroy()
        self.create_faction_select_screen()

        # Start updating the total game timer
        self.update_total_time_display()

    def start_game(self):
        """Start the game with selected factions and divide remaining time."""
        if not self.player1_faction_var.get() or not self.player2_faction_var.get():
            messagebox.showwarning("Incomplete Selection", "Please select both factions.")
            return

        # Save player information from faction select screen
        self.players[0]["faction"] = self.player1_faction_var.get()
        self.players[1]["faction"] = self.player2_faction_var.get()

        # Divide the remaining time between the two players
        self.players[0]["time"] = self.remaining_time // 2
        self.players[1]["time"] = self.remaining_time // 2

        # Destroy faction select screen and load the main game screen
        self.faction_select_frame.destroy()
        self.create_game_screen()

        # Start game loop
        self.current_player = 0
        self.turn_number = 1
        self.round_number = 1
        self.game_running = True
        self.last_update = time.perf_counter()
        self.update_time()

    def update_total_time(self):
        """Updates the total game timer."""
        if self.game_running:
            current_time = time.perf_counter()
            elapsed = current_time - self.last_update
            self.last_update = current_time
            self.remaining_time = max(0, self.total_time - (current_time - self.start_time))

            if self.remaining_time <= 0:
                self.game_running = False
                self.remaining_time = 0
                messagebox.showinfo("Game Over", "Time is up!")
                self.root.quit()
            else:
                self.root.after(1000, self.update_total_time)

    def update_remaining_time(self):
        """Updates the remaining time based on the elapsed time."""
        current_time = time.perf_counter()
        self.remaining_time = max(0, self.total_time - (current_time - self.start_time))

    def create_game_screen(self):
        """Creates the main game screen with the timer and controls."""
        # Style customization
        style = ttk.Style()
        style.configure('TLabel', background='#1e1e1e', foreground='white', font=("Arial", 18))
        style.configure('TButton', font=("Arial", 24), padding=10)
        style.configure('EndTurn.TButton', font=("Arial", 36), padding=10)

        # Create player frames
        self.player_frames = []
        self.time_labels = []
        self.vp_labels = []
        self.cp_labels = []

        for i in range(2):
            bg_color = self.faction_colors.get(self.players[i]["faction"], '#1e1e1e')
            text_color = self.get_contrast_text_color(bg_color)

            player_frame = tk.Frame(self.root, bg=bg_color, padx=20, pady=20)
            player_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

            # Player faction label
            tk.Label(player_frame, text=self.players[i]["faction"], bg=bg_color, fg=text_color, font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=10)

            # Time label
            minutes = int(self.players[i]["time"] // 60)
            seconds = int(self.players[i]["time"] % 60)
            time_str = f"{minutes:02}:{seconds:02}"
            time_label = tk.Label(player_frame, text=time_str, font=("Arial", 48), bg=bg_color, fg=text_color)
            time_label.grid(row=1, column=0, columnspan=2, pady=10)
            self.time_labels.append(time_label)

            # Victory Points
            tk.Label(player_frame, text="Victory Points:", bg=bg_color, fg=text_color).grid(row=2, column=0)
            vp_label = tk.Label(player_frame, text="0", font=("Arial", 24), bg=bg_color, fg=text_color)
            vp_label.grid(row=2, column=1)
            self.vp_labels.append(vp_label)

            # Command Points
            tk.Label(player_frame, text="Command Points:", bg=bg_color, fg=text_color).grid(row=3, column=0)
            cp_label = tk.Label(player_frame, text="0", font=("Arial", 24), bg=bg_color, fg=text_color)
            cp_label.grid(row=3, column=1)
            self.cp_labels.append(cp_label)

            # Victory and Command Point Buttons
            ttk.Button(player_frame, text="+1 VP", command=lambda i=i: self.update_points(i, "victory_points", 1)).grid(row=4, column=0, sticky="ew")
            ttk.Button(player_frame, text="-1 VP", command=lambda i=i: self.update_points(i, "victory_points", -1)).grid(row=4, column=1, sticky="ew")
            ttk.Button(player_frame, text="+1 CP", command=lambda i=i: self.update_points(i, "command_points", 1)).grid(row=5, column=0, sticky="ew")
            ttk.Button(player_frame, text="-1 CP", command=lambda i=i: self.update_points(i, "command_points", -1)).grid(row=5, column=1, sticky="ew")

            self.player_frames.append(player_frame)

        # Turn and Round labels
        self.turn_round_frame = ttk.Frame(self.root, padding="10")
        self.turn_round_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.turn_label = ttk.Label(self.turn_round_frame, text=f"Turn: 1", font=("Arial", 24))
        self.turn_label.grid(row=0, column=0, padx=10)

        self.round_label = ttk.Label(self.turn_round_frame, text=f"Round: 1", font=("Arial", 24))
        self.round_label.grid(row=0, column=1, padx=10)

        # End Turn button (Big Red Button)
        style.configure('EndTurn.TButton', font=("Arial", 36), background='red', foreground='white')
        self.end_turn_button = ttk.Button(self.root, text="End Turn", command=self.switch_player, style="EndTurn.TButton")
        self.end_turn_button.grid(row=3, column=0, columnspan=2, pady=20, ipadx=20, ipady=20)

        # Pause button
        # self.pause_button = ttk.Button(self.root, text="Pause", command=self.toggle_pause)
        # self.pause_button.grid(row=4, column=0, columnspan=2)

        # Start game loop
        self.update_display()

    def update_time(self):
        """Updates the active player's timer."""
        if self.game_running:
            current_time = time.perf_counter()
            elapsed = current_time - self.last_update
            self.last_update = current_time
            self.players[self.current_player]["time"] -= elapsed

            if self.players[self.current_player]["time"] <= 0:
                self.players[self.current_player]["time"] = 0
                self.update_display()
                self.end_game()
                return

            self.update_display()
            self.root.after(50, self.update_time)

    def update_display(self):
        """Refreshes the timers and points on the display."""
        for i in range(2):
            minutes = int(self.players[i]["time"] // 60)
            seconds = int(self.players[i]["time"] % 60)
            time_str = f"{minutes:02}:{seconds:02}"
            self.time_labels[i].config(text=time_str)
            self.vp_labels[i].config(text=str(self.players[i]["victory_points"]))
            self.cp_labels[i].config(text=str(self.players[i]["command_points"]))

    def update_points(self, player, point_type, value):
        """Updates the victory or command points for a player."""
        self.players[player][point_type] = max(0, self.players[player][point_type] + value)
        self.update_display()

    def switch_player(self):
        """Switches the active player and updates the turn and round numbers."""
        self.current_player = 1 - self.current_player
        if self.current_player == 0:
            self.round_number += 1
            self.round_label.config(text=f"Round: {self.round_number}")
        self.turn_number += 1
        self.turn_label.config(text=f"Turn: {self.turn_number}")
        self.last_update = time.perf_counter()
        self.update_display()

    def end_game(self):
        """Ends the game when a player's time runs out."""
        self.game_running = False
        winner = self.players[1 - self.current_player]['faction']
        if messagebox.askyesno("Game Over", f"{self.players[self.current_player]['faction']} has run out of time!\n\n{winner} wins!\n\nDo you want to play again?"):
            self.root.destroy()
            main()
        else:
            self.root.quit()

    def toggle_pause(self):
        """Pauses or resumes the game."""
        self.game_running = not self.game_running
        self.pause_button.config(text="Resume" if not self.game_running else "Pause")
        if self.game_running:
            self.last_update = time.perf_counter()
            self.update_time()

    def get_contrast_text_color(self, bg_color):
        """Determines the appropriate text color (black or white) based on the background color for contrast."""
        # Convert hex color to RGB
        bg_color = bg_color.lstrip('#')
        r, g, b = int(bg_color[0:2], 16), int(bg_color[2:4], 16), int(bg_color[4:6], 16)
        # Calculate luminance
        luminance = (0.299*r + 0.587*g + 0.114*b) / 255
        return 'white' if luminance < 0.5 else 'black'

def main():
    root = tk.Tk()
    app = WarClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()
