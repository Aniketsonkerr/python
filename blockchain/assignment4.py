class StoreValues:
    # Constructor to initialize and store values
    def __init__(self, id_no: int, name: str, percentage: float):
        self.id_no = id_no
        self.name = name
        self.percentage = percentage

    # Method to display the stored values
    def display_values(self):
        print("=== Stored Values Using Constructor ===")
        print(f"ID Number   : {self.id_no}")
        print(f"Name        : {self.name}")
        print(f"Percentage  : {self.percentage}%")


if __name__ == "__main__":
    # Instantiating the class and passing values to the constructor
    record = StoreValues(4227, "Aniket Sonker", 92.5)
    record.display_values()