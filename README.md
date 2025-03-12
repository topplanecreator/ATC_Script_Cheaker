Flight Plan Generator
Author: Michael Gledhill

This is a Python-based flight plan generator application built using the Tkinter library for the GUI. The program allows users to input departure and destination airport codes, route, altitude, and other flight parameters to generate a flight plan.
Features

Airport Code Lookups: The application supports many airline codes and airport codes for accurate flight plan generation.
Flight Plan Generation: Based on input parameters like departure, destination, route, and altitude, the app generates a comprehensive flight plan script.
Route Validation: If the flight is VFR (Visual Flight Rules), the route will be automatically set to "ELVIS FOUR" unless specified otherwise.
Altimeter Calculations: The application includes logic for calculating flight altitude based on direction and flight rules (VFR/IFR).
User Interface: A user-friendly interface built with Tkinter, allowing easy input and display of flight data.

Requirements

    Python 3.x
    Tkinter
    Pandas

Installation

Clone this repository to your local machine:

    git clone https://github.com/yourusername/flight-plan-generator.git

Install the required dependencies:

    pip install pandas

Usage

To run the program, simply execute the Python file:

python flight_plan_generator.py

The program will open a window where you can enter the following parameters:

Frequency: Enter the frequency for the departure (default is 125.8).
Callsign: Enter the airline code and flight number (e.g., AAL123).
Departure and Destination: Enter the ICAO codes of the departure and destination airports (e.g., KSFO). 
Route: Select the route from the available options.
Altitude: Enter the desired altitude.
VFR/IFR: Select whether the flight is under VFR or IFR rules.
Squawk: Enter the squawk code for the flight.

Once all fields are filled, click on "Generate Flight Plan" to generate the flight plan. The results will appear in the output section.
Example
Input:

Callsign: AAL123
Departure: KMEM
Destination: KORD
Route: ELVIS FOUR
Altitude: 240
VFR/IFR: IFR
Squawk: 3456

Output:

American Airlines 123 Memphis Ground, cleared to ORD, via ELVIS FOUR,
then as filed, maintain 5000, expect FL 250 10 minutes after departure,
departure frequency 125.8, squawk 3456

Contributing

Fork the repository
Create your feature branch (git checkout -b feature-branch)
Commit your changes (git commit -am 'Add new feature')
Push to the branch (git push origin feature-branch)
Create a new Pull Request

License

This project is licensed under the MIT License - see the LICENSE file for details.




Prerequisites

Before you begin, ensure you have the following installed:
Python 3 (Preferably installed via Homebrew)
    brew install python
pyinstaller (Used for packaging the executable)
    pip install pyinstaller

Steps to Compile the Application

1. Navigate to Your Project Directory
    cd Downloads/ATC_Script_Cheaker/

2. Run PyInstaller to Create an Executable
    pyinstaller --onefile --windowed --name FlightPlanGenerator main.py

--onefile: Packages everything into a single executable file.
--windowed: Hides the terminal (useful for GUI applications; remove for CLI tools).
--name FlightPlanGenerator: Specifies the output name
The generated files will be in the dist/ directory.

3. (Optional) Add an App Icon
Convert your icon to .icns format using: