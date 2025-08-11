<img width="100%" alt="Beard Wizard Banner" src="https://github.com/user-attachments/assets/517ad8e9-ad22-457d-9538-a9e62d137cd7" />

# Beard Wizard 🎯

## Basic Details
### Team Name: Half Baked

### Team Members
- Team Lead: Nijoy P Jose - Vidya Acadmy of Science and Technology, Thrissur
- Member 2: Albin Antony - Vidya Acadmy of Science and Technology, Thrissur

### Project Description
Beard Wizard is an AI-powered web application that acts as a "magic mirror" for beard grooming. Using a live webcam feed, it overlays precise, real-time cutting guides for various beard styles directly onto your face, ensuring a perfectly symmetrical trim every time.

### The Problem (that doesn't exist)
The crippling anxiety of an uneven beard trim. Every year, millions of men face the mirror, trimmer in hand, only to emerge with a lopsided monstrosity. The emotional toll is immeasurable, leading to a global crisis of confidence and an over-reliance on expensive barbers.

### The Solution (that nobody asked for)
We've weaponized AI and computer vision to fight back. Beard Wizard streams a live video of your face from your Django server, runs it through a sophisticated Python/OpenCV backend, and draws the perfect beard outline for you to follow. It's like having a tiny, digital barber living in your computer, guiding your every move.

## Technical Details
### Technologies/Components Used
For Software:
- **Languages:** Python, JavaScript, HTML, CSS
- **Frameworks:** Django
- **Libraries:** OpenCV (`opencv-python`), MediaPipe, NumPy
- **Styling:** Tailwind CSS

For Hardware:
- A standard webcam (the one on your laptop is perfect)

### Implementation
For Software:
# Installation
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/NIJOY-P-JOSE/beard-wizard
    ```
2.  **Navigate to Project Directory:**
    ```bash
    cd beard-wizard
    ```
3.  **Create and Activate a Virtual Environment:**
    * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
4.  **Install Required Packages:**
    Use the provided `requirements.txt` file to install all dependencies at once.
    ```bash
    pip install -r requirements.txt
    ```

# Run
1.  **Start the Django Server:**
    Make sure you are in the main project directory where `manage.py` is located.
    ```bash
    python manage.py runserver
    ```
2.  **View the Application:**
    Open your web browser and navigate to the following address:
    `http://12.0.0.1:8000/`

### Project Documentation
For Software:

# Screenshots
<img width="1918" height="807" alt="image" src="https://github.com/user-attachments/assets/0ef8458b-e41f-40a9-b8f3-d5f2debea08e" />
<img width="1918" height="927" alt="image" src="https://github.com/user-attachments/assets/62dc36d2-3412-45db-9e0e-63b64108e415" />

*The stylish and modern homepage of Beard Wizard.*

![WhatsApp Image 2025-08-09 at 4 46 42 PM](https://github.com/user-attachments/assets/60cf8ac1-0b3d-4442-8085-bdb8ad227af0)
*A user selecting the "Classic Full Beard" style from the control panel.*

# Diagrams
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/933b27a3-ab60-44e2-a252-95d5d3afbae8" />

*Our high-level architecture: The browser displays a video stream from a Django URL, which is generated in real-time by a Python view using OpenCV and MediaPipe to process webcam frames.*

### Project Demo
# Video
https://github.com/user-attachments/assets/c757e817-5b63-440e-bc18-17f44f13a8f0
*This video demonstrates the core feature: a user accessing the web app, starting the trimming guide, and switching between different beard style overlays in real-time.*

## Team Contributions
- **Nijoy P Jose**: Backend development (Django setup, Python/OpenCV logic), AI integration with MediaPipe, and video streaming implementation.
- **Albin Antony**: Frontend development (HTML, Tailwind CSS), user interface design, and creating the overall user experience.

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--25-25?link=https%3A%2F%2Fwww.tinkerhub.org%2Fevents%2FQ2Q1TQKX6Q%2FUseless%2520Projects)
