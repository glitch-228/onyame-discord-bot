# Onyame Discord Bot

Discord bot that provides random anime from an anime site
currently:'animekai.to'

---

## Features

*   **/new**: Displays the 12 most recently updated anime series. You can navigate through the list using "Previous" and "Next" buttons.
*   [NEW]**/random [amount]**: Shows a specified number of random anime titles (default is 1, max is 30). You can navigate through the list using "Previous" and "Next" buttons.

---

## Tech Stack

*   Python 3.12
*   py-cord
*   requests
*   beautifulsoup4
*   python-dotenv

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/glitch-228/onyame-discord-bot
    cd onyame-discord-bot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file and add your bot token:**
    ```
    TOKEN=your_discord_bot_token
    ```

4.  **Run the bot:**
    ```bash
    python main.py
    ```

---

## Demo

![demo](image.png)
