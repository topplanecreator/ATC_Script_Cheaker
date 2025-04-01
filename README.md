# Flight Plan Generator

This Python application, built with Tkinter, generates flight plans for both IFR (Instrument Flight Rules) and VFR (Visual Flight Rules) flights. It reads airline codes, airport data, and route information from CSV files and allows users to input flight details through a graphical user interface (GUI).

## Features

-   **IFR Flight Plan Generation:**
    Calculates headings and altitudes based on departure and destination airports.
    Provides route selection from a dropdown menu.
    Supports airline callsign input with automatic airline name lookup.
    Generates flight plan text with all necessary information.
    Displays system notes for potential issues.
-   **VFR Flight Plan Information:**
    Provides information on VFR flight clearances.
    Includes a button that opens a website.
-   **Note Taking:**
    Allows users to take notes with text coloring options.
    Saves and loads notes to and from a JSON file.
-   **User-Friendly GUI:**
    Organized layout with tabs for IFR and VFR.
    Clear labels and input fields.

## Files

-   `airlines.csv`: Contains airline codes and names.
-   `airports.csv`: Contains airport data (ICAO codes, names, latitudes, longitudes).
-   `routes.csv`: Contains route names and fix names.
-   `user_notes.json`: Stores user notes, tag ranges, and tag colors.

## Dependencies

-   `tkinter`: For the GUI.
-   `pandas`: For data manipulation (CSV reading).
-   `math`: For calculations.
-   `csv`: For reading CSV files.
-   `webbrowser`: For opening links.
-   `json`: For reading and writing json files.
-   `ttk`: For themed widgets.

## How to Run

1.  **Make sure you have Python installed.** If you don't, you can download it from the official Python website (python.org). Just follow the instructions on the site to install it.

2.  **Install the needed library.** This program uses a tool called "pandas" to work with the data files. To install it:

    * **On Windows:**
        * Open the Command Prompt. You can do this by searching for "cmd" in the Windows search bar.
        * Type one of these commands and press Enter:
            ```bash
            pip install pandas
            ```
            Or, if that doesn't work, try:
            ```bash
            pip3 install pandas
            ```
    * **On macOS or Linux:**
        * Open the Terminal.
        * Type one of these commands and press Enter:
            ```bash
            pip install pandas
            ```
            Or, if that doesn't work, try:
            ```bash
            pip3 install pandas
            ```
        One of these commands should work!

3.  **Place the data files in the correct spot.** You need to put the `airlines.csv`, `airports.csv`, and `routes.csv` files in the same folder as the Python script.

4.  **Find the folder.**
    * **If you downloaded a .zip file:**
        * Unzip (extract) the file and put the extracted folder into your Downloads folder.
    * **Go to the folder using your command prompt or terminal:**
        * **On Windows:**
            * If you placed the folder in your downloads, type this into your command prompt, and press enter.
                ```bash
                cd Downloads/ATC_Script_Cheaker-main
                ```
        * **On macOS or Linux:**
            * If you placed the folder in your downloads, type this into your terminal, and press enter.
                ```bash
                cd Downloads/ATC_Script_Cheaker-main
                ```
            * If you downloaded the file to a different folder, change "Downloads" to the name of the folder where you put it.

5.  **Run the program.**
    * In the same command prompt or terminal window, type this and press Enter:
        ```bash
        python KMEM_ATC.py
        ```
    * If that doesn't work, try:
        ```bash
        python3 KMEM_ATC.py
        ```

## Usage

### IFR Tab

1.  Enter the frequency, callsign, departure ICAO code, destination ICAO code, altitude, and squawk code.
2.  Select the aircraft type and route from the dropdown menus.
3.  Click the "Update Flight Plan" button to generate the flight plan.
4.  The generated flight plan, heading, and direction will be displayed.
5.  System notes will appear below the flight plan, if any.

### VFR Tab

1.  Read the VFR flight plan information.
2.  Click the "Click me!" button to open a link.

### Notes Section

1.  Type your notes in the "Your Notes" text box.
2.  Select text and click a color button to change the text color.
3.  Notes are automatically saved when the application is closed.

## Note about the code.

The code is designed to be easy to read and understand, with comments explaining each section. Error handling is included to manage potential issues like missing files or invalid input. The GUI is built using Tkinter, providing a simple and intuitive interface.

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues for bug reports or feature requests.

## License

This project is open source.