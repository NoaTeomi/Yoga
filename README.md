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

# Project Setup

Follow these steps to successfully run the Yoga project from the Git repository.

**Prerequisites:**

**1. Install Docker and Docker Compose**

Docker and Docker Compose are required to run this project. Follow the official installation instructions based on your operating system:

- Docker: Install Docker
- Docker Compose: Install Docker Compose (if not included with Docker)

  Note: After installing Docker, make sure Docker is running. You can verify by running:
  
       docker --version
       docker-compose --version

# Steps to Run the Project

**1. Clone the Repository**

Start by cloning the project repository from GitHub:

      git clone https://github.com/noateomi/Yoga.git
      cd Yoga

**2. Build and Run the Docker Containers**

Run the following command to build and start the containers:

      docker-compose up -d --build

This will:

- Build the Docker image based on the Dockerfile.
- Start the web and nginx services defined in docker-compose.yml.

**3. Load Initial Data for Yoga Poses**

To load sample data (including images) into your database, run the following command:

      docker-compose exec web python Yoga/manage.py loaddata /app/Yoga/yoga_poses_fixture.json 

This command loads initial data for the YogaPose model to ensure the app displays sample yoga poses.

**4. Access the Application**

Once everything is set up, access the application by opening a browser and going to:

     http://localhost:8080

- The application will be accessible on port 8080, with Nginx as the reverse proxy.
- The web service serves the Django application, and nginx serves static files.

**5. Stopping the Application**

To stop the running containers, use:

      docker-compose down
    
