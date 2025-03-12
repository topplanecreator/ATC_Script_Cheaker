# Flight Plan Generator

## Author: Michael Gledhill

This is a Python-based flight plan generator application built using the Tkinter library for the GUI. The program allows users to input departure and destination airport codes, route, altitude, and other flight parameters to generate a flight plan.

## Features

- **Airport Code Lookups**: The application supports many airline codes and airport codes for accurate flight plan generation.
- **Flight Plan Generation**: Based on input parameters like departure, destination, route, and altitude, the app generates a comprehensive flight plan script.
- **Route Validation**: If the flight is VFR (Visual Flight Rules), the route will be automatically set to "ELVIS FOUR" unless specified otherwise.
- **Altimeter Calculations**: The application includes logic for calculating flight altitude based on direction and flight rules (VFR/IFR).
- **User Interface**: A user-friendly interface built with Tkinter, allowing easy input and display of flight data.

## Requirements

- Python 3.x
- Tkinter
- Pandas

## Installation

Clone this repository to your local machine:

```sh
git clone https://github.com/yourusername/flight-plan-generator.git
```

Install the required dependencies:

```sh
pip install pandas
```

## Usage

To run the program, simply execute the Python file:

```sh
python flight_plan_generator.py
```

The program will open a window where you can enter the following parameters:

- **Frequency**: Enter the frequency for the departure (default is 125.8).
- **Callsign**: Enter the airline code and flight number (e.g., AAL123).
- **Departure and Destination**: Enter the ICAO codes of the departure and destination airports (e.g., KSFO). 
- **Route**: Select the route from the available options.
- **Altitude**: Enter the desired altitude.
- **VFR/IFR**: Select whether the flight is under VFR or IFR rules.
- **Squawk**: Enter the squawk code for the flight.

Once all fields are filled, click on "Generate Flight Plan" to generate the flight plan. The results will appear in the output section.

### Example

#### Input:
```
Callsign: AAL123
Departure: KMEM
Destination: KORD
Route: ELVIS FOUR
Altitude: 240
VFR/IFR: IFR
Squawk: 3456
```

#### Output:
```
American Airlines 123 Memphis Ground, cleared to ORD, via ELVIS FOUR,
then as filed, maintain 5000, expect FL 250 10 minutes after departure,
departure frequency 125.8, squawk 3456
```

## Contributing

1. Fork the repository.
2. Create your feature branch:
   ```sh
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```sh
   git commit -am 'Add new feature'
   ```
4. Push to the branch:
   ```sh
   git push origin feature-branch
   ```
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

# Flight Plan Generator - macOS Compilation Guide

This guide explains how to compile the Python-based Flight Plan Generator into a standalone macOS application.

## macOS Compilation Guide

### Prerequisites
Ensure you have the following installed:

- **Python 3** (Recommended installation via [Homebrew](https://brew.sh/))  
  ```sh
  brew install python
  ```
- **`pyinstaller`** (For packaging the executable)  
  ```sh
  pip install pyinstaller
  ```
- **Project Dependencies** (Install from `requirements.txt`)  
  ```sh
  pip install -r requirements.txt
  ```

### Compilation Steps

1. **Navigate to Your Project Directory**  
   ```sh
   cd /path/to/your/project
   ```

2. **Run PyInstaller to Create an Executable**  
   ```sh
   pyinstaller --onefile --windowed --name FlightPlanGenerator main.py
   ```

3. **(Optional) Add an App Icon**  
   ```sh
   pyinstaller --onefile --windowed --name FlightPlanGenerator --icon=icon.icns main.py
   ```

4. **Code Sign the Application (If Needed)**  
   ```sh
   codesign --force --deep --sign - dist/FlightPlanGenerator.app
   ```

5. **Test the Executable**  
   ```sh
   ./dist/FlightPlanGenerator
   ```

6. **Package for Distribution**  
   ```sh
   hdiutil create -volname "FlightPlanGenerator" -srcfolder "dist/FlightPlanGenerator.app" -ov -format UDZO FlightPlanGenerator.dmg
   ```

---

# Flight Plan Generator - Windows Compilation Guide

### Prerequisites
Ensure you have the following installed:

- **Python 3** (Download from [python.org](https://www.python.org/downloads/))
- **`pyinstaller`** (For packaging the executable)  
  ```sh
  pip install pyinstaller
  ```
- **Project Dependencies** (Install from `requirements.txt`)  
  ```sh
  pip install -r requirements.txt
  ```

### Compilation Steps

1. **Navigate to Your Project Directory**  
   ```sh
   cd C:\path\to\your\project
   ```

2. **Run PyInstaller to Create an Executable**  
   ```sh
   pyinstaller --onefile --windowed --name FlightPlanGenerator main.py
   ```

3. **(Optional) Add an App Icon**  
   ```sh
   pyinstaller --onefile --windowed --name FlightPlanGenerator --icon=icon.ico main.py
   ```

4. **Test the Executable**  
   ```sh
   dist\FlightPlanGenerator.exe
   ```

5. **Create an Installer (Optional)**  
   Use a tool like Inno Setup or NSIS to package the `.exe` into an installer.

## Troubleshooting
- If Windows Defender blocks the app, allow it in security settings.
- If missing DLLs occur, try adding `--add-data` flags to include dependencies.

---

For additional issues, check the PyInstaller [documentation](https://pyinstaller.org/).
