# This program runs on the PC and communicates with the sensor board over USB.
# Before running it, update PORT to match the board's port in Device Manager.
# Install the serial dependency with: pip install pyserial
# Close other programs that may already be using the board's serial port.

import sqlite3
import time

import serial

PORT = "COM4"
BAUD = 115200
DATABASE_NAME = "sensor_data.db"


def ask_board(ser, command):
    """Send a one-letter command and return the numeric value in the board's reply."""
    # This function sends a command to the sensor board and waits for the board to
    # respond with measured data. It ignores any old serial data before sending so
    # the reply matches the current request.
    ser.reset_input_buffer()
    ser.write((command + "\n").encode())

    # Keep reading lines until the board sends a valid DATA response. The board may
    # send startup messages first, so we ignore anything that is not a DATA line.
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line == "":
            raise TimeoutError("No reply from board")
        if line.startswith("DATA,"):
            return float(line.split(",")[2])


class DatabaseManager:
    """Create the sensor history table and provide methods to save and display it."""

    def __init__(self, database_name=DATABASE_NAME):
        # This constructor opens the SQLite database and creates the table that will
        # store every reading. If the database file does not exist yet, SQLite will
        # create it automatically.
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

        # Create a table with an ID, a timestamp, the sensor name, and the numeric
        # reading value. This keeps each record organized and easy to view later.
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                sensor_type TEXT NOT NULL,
                reading_value REAL NOT NULL
            )
            """
        )
        self.connection.commit()

    def log_reading(self, sensor_type, reading_value):
        """Insert one sensor reading and its local date/time into the database."""
        # This method records one reading at the current time so the data can be
        # reviewed later in chronological order.
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            """
            INSERT INTO sensor_readings (timestamp, sensor_type, reading_value)
            VALUES (?, ?, ?)
            """,
            (timestamp, sensor_type, reading_value),
        )
        self.connection.commit()

    def display_history(self):
        """Print every stored reading in the order it was recorded."""
        # This method fetches all saved readings and prints them neatly. It reads the
        # records in their insertion order so the log is easy to follow.
        self.cursor.execute(
            """
            SELECT id, timestamp, sensor_type, reading_value
            FROM sensor_readings
            ORDER BY id
            """
        )
        records = self.cursor.fetchall()

        if not records:
            print("No sensor readings have been logged.")
            return

        print("\nSensor reading history:")
        print("ID | Timestamp           | Sensor      | Reading")
        print("-" * 56)
        for record_id, timestamp, sensor_type, reading_value in records:
            print(
                f"{record_id} | {timestamp} | {sensor_type:<11} | "
                f"{reading_value}"
            )

    def close(self):
        """Release the SQLite connection when the program is ending."""
        # This method closes the database connection so the file is properly freed
        # and no database lock remains open.
        self.connection.close()


def read_temperature(ser, database_manager):
    """Request, display, and save one temperature reading from the board."""
    # This function asks the board for the temperature, prints it for the user, and
    # stores it in the database for later review.
    temperature = ask_board(ser, "T")
    print(f"Temperature: {temperature:.1f} C")
    database_manager.log_reading("Temperature", temperature)


def read_humidity(ser, database_manager):
    """Request, display, and save one humidity reading from the board."""
    # This function asks the board for humidity, prints the result, and saves it in
    # the database as a new log entry.
    humidity = ask_board(ser, "H")
    print(f"Humidity: {humidity:.1f} %")
    database_manager.log_reading("Humidity", humidity)


def display_menu():
    """Show the available commands before each prompt."""
    # This function outputs the menu choices so the user knows what commands are
    # available in the current session.
    print(
        "Please choose from the following options:\n"
        "  T - Temperature\n"
        "  H - Humidity\n"
        "  0 - Both\n"
        "  V - View Log History"
    )


def main():
    # This is the main loop of the program. It keeps the app running until the user
    # closes it, handling menu choices and sensor requests in one continuous cycle.
    database_manager = DatabaseManager()
    ser = None

    try:
        # The program keeps showing the menu and asking for input until the user
        # decides to stop. Invalid entries are ignored without reading the sensor.
        while True:
            display_menu()
            choice = input("Enter your choice: ").strip().upper()

            if choice not in {"T", "H", "0", "V"}:
                print("Invalid choice. Please enter T, H, 0, or V.\n")
                continue

            if choice == "V":
                database_manager.display_history()
                continue

            # Open the serial connection only when a real reading is requested. The
            # board may reset when the connection starts, so we give it a moment.
            if ser is None:
                ser = serial.Serial(PORT, BAUD, timeout=3)
                time.sleep(2)
                ser.reset_input_buffer()

            if choice == "T":
                read_temperature(ser, database_manager)
            elif choice == "H":
                read_humidity(ser, database_manager)
            else:  # "0" means take and save both readings.
                read_temperature(ser, database_manager)
                read_humidity(ser, database_manager)

            print()
    finally:
        # Clean up all resources when the program ends, even if there is an error or
        # the user interrupts the loop.
        if ser is not None:
            ser.close()
        database_manager.close()


if __name__ == "__main__":
    main()
