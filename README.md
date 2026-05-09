# Soul Steep: An Intern's Trial
## Project Description
- Project by: Varissara Arayavilaipong
- Game Genre: Simulation, Narrative

Soul Steep is a simulation and narrative game where you play as a newly deceased intern at a mysterious afterlife tea shop. Over 7 in-game days, restless spirits arrive one by one, each carrying unresolved emotions. The player must read cryptic diary fragments written by each spirit, diagnose their emotional state, and brew a personalised therapeutic tea using a three-step ingredient system — choosing a Base Water, a Tea Bag, and a Topping — each of which carries a real numerical impact on the final brew. The concept of a tea shop as a place of rest for wandering souls was inspired by the novel Under the Whispering Door by TJ Klune.

---
## Installation
To clone this project:
```sh
git clone https://github.com/<username>/soul-steep.git
```
To create and run a Python environment for this project:

**Windows:**
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
**Mac:**
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---
## Running Guide
After activating the Python environment, run the game with:

**Windows:**
```bat
python main.py
```
**Mac:**
```sh
python3 main.py
```
To open the data dashboard separately (requires at least one completed session):
```sh
python data_game.py
```

---
## Tutorial / Usage
1. **Title Screen** — Choose New Game, Continue (if a save exists), Statistic (if data exists), or Exit.
2. **Daily Letter** — Each day begins with a letter from the Manager. Click outside the card to dismiss it.
3. **Reading Hints** — Click the four coloured buttons at the top of the screen to read each spirit's diary fragments. Use the emotional intensity of the writing to rank their four emotions from strongest (Level 30) to weakest (Level 5).
4. **Brewing** — Follow this order:
   - Click the **Kettle** to create a teapot
   - Choose a **Base Water** (matches strongest emotion, +30 points)
   - Choose a **Tea Bag** (matches second emotion, +20 points)
   - Choose a **Topping** (adds +10 to one emotion and +5 to another)
5. **Serving** — Click **SERVE** to submit your brew. Your Accuracy score is calculated immediately.
6. **Mistakes** — Click **DELETE** to scrap the teapot and start over before serving.
7. **Pause** — Press **ESC** or click the ‖ button to pause. The pause menu includes a volume slider.
8. **Goal** — Serve 5 spirits per day for 7 days. Keep your average Accuracy above 70% to pass the evaluation.

---
## Game Features
- **Emotional Diagnosis System** — Each spirit has four hidden emotion values (5, 10, 20, or 30). Interpret literary diary clues to infer the values rather than being told them directly.
- **Three-Step Brewing** — Every ingredient choice carries a real numerical impact on the brew's emotional profile. Water (+30), Tea Bag (+20), Topping (+10/+5 cross-effect).
- **7-Day Narrative Arc** — Daily letters from Manager Grimoire build a sarcastic and darkly funny story as you work toward your final evaluation.
- **Two Endings** — A Pass or Fail ending determined by your overall average accuracy across all 35 spirits, each with unique manager dialogue.
- **Dynamic BGM** — Background music shifts between three tracks (calm, main, tense) based on your running average accuracy.
- **Data Dashboard** — A separate tkinter window visualises your gameplay data across sessions with five interactive charts and descriptive statistics.
- **Save System** — Progress is saved automatically between days and can be continued from the title screen.

---
## Known Bugs
- The data dashboard (`data_game.py`) opens in a separate tkinter window rather than inside the pygame window, so the game window remains visible behind it with no indication the game is paused.
- Font fallback behaviour may vary on systems without Comic Sans MS or Segoe Print installed — the game will fall back to the pygame default font, which affects visual style but not functionality in case using Mac to play this game.

---
## Unfinished Works
- All planned features from the project proposal have been implemented. 
---
## External Sources
**Music:**
1. *Hyperfun* — Kevin MacLeod, incompetech.com — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — https://youtu.be/Vugj1cii9Y0
2. *Source d'Amour* — Arthur-Marie Brillouin, soundcloud.com/amariamusique — [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/) — https://youtu.be/BtOc2Uo46hI
3. *Winter Waltz* — Scott Buckley, scottbuckley.com.au — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — https://youtu.be/FdjMtzmVOGI

**Sound Effects:**
4. *611675__genel__sprinkle.wav* — genel — Creative Commons — https://freesound.org/s/611675/

**Libraries:**
5. `pygame` — https://www.pygame.org
6. `matplotlib` — https://matplotlib.org
7. `Pillow` — https://python-pillow.org
8. `numpy` — https://numpy.org
