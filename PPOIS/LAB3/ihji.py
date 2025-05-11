
class Publisher:

    def __init__(self, title: str, company: str, year: int, content: str):
        try:
            self.title = title
            self.company = company

            if year > 2025:
                raise ValueError(f"Year should be valid")
            self.year = year
            self.content = content
        except ValueError as e:
            raise ValueError("initialization error")



def main():
    pub = Publisher("negr", "1", 2022, "srjgosg")
    print(pub)


if __name__ == "__main__":
    main()

