# Yoga Asanas Gallery - Sequencing Project
This is a Django-based web application that allows users to browse a gallery of yoga poses and create personalized sequences.
The application provides functionality for registered users to save, edit, and delete their custom yoga pose sequences, 
all while maintaining a smooth user experience.

Features
1. Yoga Asanas Gallery
  * A public gallery of yoga poses where each pose includes a name and an image.
  * Logged-out users can view the gallery, but to create sequences, they need to sign in or sign up.
2. User Authentication
  * Users can register, log in, and log out of their accounts.
  * Logged-in users have access to personalized features such as sequence creation, editing, and deletion.

3. Sequence Creation
  * Users can create custom yoga sequences by selecting from available yoga poses in the gallery.
  * Sequences can be saved to the user’s account for future use.
  * Images included: While creating a sequence, pose images are displayed for easy reference.

4. My Sequences
  * Registered users can view, edit, or delete their saved sequences.
  * A simple interface for managing personal yoga sequences with just a few clicks.

# How to Run

1. Clone the repository:

    ```bash
    git clone https://github.com/noateomi/Yoga.git
    cd Yoga
    ```

2. Start the Docker containers:

    ```bash
    docker compose up -d
    ```

The application will be accessible at:
- **Web**: [http://localhost:8000](http://localhost:8000)
- **Nginx**: [http://localhost:8080](http://localhost:8080)

