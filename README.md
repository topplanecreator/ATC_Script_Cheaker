# Flight Plan Generator

## Author: Michael Gledhill

This is a Python-based flight plan generator application built using the Tkinter library for the GUI. The program allows users to input departure and destination airport codes, route, altitude, and other flight parameters to generate a flight plan.

## Features

- **Airport Code Lookups**: The application supports many airline and airport codes for accurate flight plan generation.
- **Flight Plan Generation**: Based on input parameters like departure, destination, route, and altitude, the app generates a comprehensive flight plan script.
- **Route Validation**: If the flight is VFR (Visual Flight Rules), the route will automatically default to "ELVIS FOUR" unless specified otherwise.
- **Altitude Calculations**: The application includes logic for determining flight altitude based on direction and flight rules (VFR/IFR).
- **User-Friendly Interface**: A simple and intuitive GUI built with Tkinter for easy input and display of flight data.

## Installation

### Requirements
- Python 3.x
- Tkinter
- Pandas

### Clone the Repository
```sh
git clone https://github.com/yourusername/flight-plan-generator.git
```

### Install Dependencies
```sh
pip install pandas
```

## Usage
To run the program, execute the Python script:
```sh
python flight_plan_generator.py
```

### Input Parameters
- **Frequency**: Enter the departure frequency (default is 125.8).
- **Callsign**: Enter the airline code and flight number (e.g., AAL123).
- **Departure and Destination**: Enter the ICAO codes of the airports (e.g., KSFO).
- **Route**: Select the route from available options.
- **Altitude**: Enter the desired altitude.
- **VFR/IFR**: Choose whether the flight operates under VFR or IFR.
- **Squawk**: Enter the squawk code for the flight.

Once all fields are filled, click "Generate Flight Plan" to create the flight plan, which will be displayed in the output section.

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
departure frequency 125.8, squawk 3456.
```

## Running on macOS

If you encounter permission issues when running the app, use the following command:
```sh
xattr -c <path/to/application.app>
```
For a detailed explanation, watch this [video guide](https://www.youtube.com/watch?v=ZH8_XHzkKD4).

If you're not comfortable running this command, you can compile the application yourself following the instructions below.

---

# Compilation Guides

## macOS Compilation Guide

### Prerequisites
- **Python 3** (Install via [Homebrew](https://brew.sh/))  
  ```sh
  brew install python
  ```
- **`pyinstaller`** (For packaging the executable)  
  ```sh
  pip install pyinstaller
  ```
- **Project Dependencies**  
  ```sh
  pip install -r requirements.txt
  ```

### Compilation Steps
1. Navigate to your project directory:
   ```sh
   cd /path/to/your/project
   ```
2. Run PyInstaller to create an executable:
   ```sh
   pyinstaller --onefile --windowed --name FlightPlanGenerator main.py
   ```
3. (Optional) Add an app icon:
   ```sh
   pyinstaller --onefile --windowed --name FlightPlanGenerator --icon=icon.icns main.py
   ```
4. Code sign the application (if needed):
   ```sh
   codesign --force --deep --sign - dist/FlightPlanGenerator.app
   ```
5. Test the executable:
   ```sh
   ./dist/FlightPlanGenerator
   ```
6. Package for distribution:
   ```sh
   hdiutil create -volname "FlightPlanGenerator" -srcfolder "dist/FlightPlanGenerator.app" -ov -format UDZO FlightPlanGenerator.dmg
   ```

---

## Windows Compilation Guide

### Prerequisites
- **Python 3** (Download from [python.org](https://www.python.org/downloads/))
- **`pyinstaller`** (For packaging the executable)  
  ```sh
  pip install pyinstaller
  ```
- **Project Dependencies**  
  ```sh
  pip install -r requirements.txt
  ```

### Compilation Steps
1. Navigate to your project directory:
   ```sh
   cd C:\path\to\your\project
   ```
2. Run PyInstaller to create an executable:
   ```sh
   pyinstaller --onefile --windowed --name FlightPlanGenerator main.py
   ```
3. (Optional) Add an app icon:
   ```sh
   pyinstaller --onefile --windowed --name FlightPlanGenerator --icon=icon.ico main.py
   ```
4. Test the executable:
   ```sh
   dist\FlightPlanGenerator.exe
   ```
5. (Optional) Create an installer using Inno Setup or NSIS.

### Troubleshooting
- If Windows Defender blocks the app, allow it in security settings.
- If missing DLLs occur, try adding `--add-data` flags to include dependencies.

For further assistance, check the [PyInstaller documentation](https://pyinstaller.org/).

---

## Contributing
1. Fork the repository.
2. Create a feature branch:
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

