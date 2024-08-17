
# Triateamo

**Triateamo** is a console-based assistant bot for managing contacts. With this bot, you can add, modify, delete, and search contacts by various parameters such as name, phone number, or birthday.

## Installation and Setup

Before using Triateamo, you need to set up a virtual environment and install the required dependencies.

### 1. Clone the Repository

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/vdubyna/go-it-team-project.git
cd triateamo
```

### 2. Create a Virtual Environment

Create a virtual environment to isolate your project's dependencies:

```
python -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment before installing dependencies:

- **Windows:**

```bash
venv\Scripts\activate
```

- **macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

Once the virtual environment is activated, install the necessary dependencies using the \`requirements.txt\` file:

```bash
pip install -r requirements.txt
```

### 5. Running the Application

After installing the dependencies, you can run the Triateamo bot using:

```bash
python main.py
```

## Features

- **Add Contacts:** Easily add new contacts with name, phone number, and birthday.
- **Update Contacts:** Modify existing contact information.
- **Search Contacts:** Search for contacts by name, phone number, or birthday.
- **View All Contacts:** Display all contacts in your address book.
- **Birthday Notifications:** View upcoming birthdays to never miss an important date.
- **Manage Tags:** Add or remove tags from contacts, helping categorize and organize your contacts more effectively.
- **Add Notes:** Create, edit, and delete notes associated with your contacts or independently.
- **Search Notes:** Search for notes by title, content, or tags to quickly find relevant information.
- **Show All Notes:** Display a table of all notes, providing a quick overview of your saved notes.
- **Search Contacts with Tags:** Allows users to search for contacts by tags, making it easier to find grouped contacts.

## Usage

Upon running the bot, you'll be presented with a menu of options. Use the arrow keys to navigate and press Enter to select an option. Follow the on-screen prompts to perform actions such as adding or searching for contacts.

## Contributing

If you'd like to contribute to Triateamo, feel free to fork the repository and submit a pull request. We welcome all improvements and bug fixes!
