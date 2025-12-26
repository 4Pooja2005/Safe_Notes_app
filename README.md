# Safe Notes

**Safe Notes** is a simple desktop application for creating, saving, and managing personal notes securely. Each user can create an account with a username and password, and all notes are stored locally on the computer.  

---

## Features

- Secure login and registration system  
- Create, edit, and delete notes  
- Light and dark mode toggle  
- Show/hide password while typing  
- Forgot password feature is **not yet implemented** (planned for future improvements)  

---

## How to Use

1. **Download and Open the App**  
   Run the `SafeNotes.exe` file on your Windows machine. Windows will not let it run naturally, just click on "Run anyway"  

2. **Login or Register**  
   - Enter a username and password  
   - If the username does not exist, the app will create a new account.
   - But if password is wrong, you get prompted to try again (currently unlimited times)  

3. **Manage Notes**  
   - Enter a note title and content  
   - Click **Save** to store the note  
   - Select a note from the list to edit or delete it  

4. **Theme**  
   Toggle between light and dark mode using the button on the left panel  

5. **Logout**  
   Click **Logout** to return to the login screen  

---

## Where Notes Are Stored

All user accounts and notes are stored locally in a `data` folder next to the application. Nothing is uploaded to the internet, ensuring privacy.  

---

## System Requirements

- Windows 10 or 11  
- 64-bit architecture  
- No additional software installation required  

---

## Tech Stack

- Python 3.x  
- Tkinter for the GUI  
- JSON for local data storage  
