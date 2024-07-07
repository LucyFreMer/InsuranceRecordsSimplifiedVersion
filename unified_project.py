import re


# třída pro reprezentaci pojištěné osoby
class InsuredPerson:
    def __init__(self, first_name: str, last_name: str, age: int, phone_number: str) -> None:
        # Inicializace atributů pojištěné osoby
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.phone_number = phone_number

    def __str__(self):
        # Vrácení textové reprezentace pojištěné osoby
        return f"{self.first_name} {self.last_name}, věk: {self.age}, telefonní číslo: {self.phone_number}"


# třída pro správu kolekce pojištěných osob
class InsuranceRegistry:
    def __init__(self, insured_people: list[InsuredPerson] = None) -> None:
        if insured_people is None:
            insured_people = []
        self.__insured_people = insured_people

    def add_insured_person(self, person: InsuredPerson) -> None:
        # Přidání pojištěné osoby do seznamu
        self.__insured_people.append(person)

    def list_insured_people(self) -> list[InsuredPerson]:
        # Vrácení seznamu všech pojištěných osob
        return self.__insured_people

    def get_insured_person(self, first_name, last_name) -> list[InsuredPerson]:
        # Vyhledání pojištěné osoby podle jména a příjmení
        return [
            p for p in self.__insured_people
            if p.first_name.lower() == first_name and p.last_name.lower() == last_name
        ]


# třída pro zpracování vstupů od uživatele
class InsuranceForm:
    def get_first_name(self) -> str:
        # Získání a validace křestního jména, aby nebylo prázdné a neobsahovalo žádná čísla
        while True:
            first_name = input("Zadejte křestní jméno: ").strip()
            if first_name == "":
                print("Křestní jméno nesmí být prázdné.")
            elif any(char.isdigit() for char in first_name):
                print("Křestní jméno nesmí obsahovat číslice.")
            else:
                break
        return first_name

    def get_last_name(self) -> str:
        # Získání a validace příjmení, aby nebylo prázdné a neobsahovalo žádná čísla
        while True:
            last_name = input("Zadejte příjmení: ").strip()
            if last_name == "":
                print("Příjmení nesmí být prázdné.")
            elif any(char.isdigit() for char in last_name):
                print("Příjmení nesmí obsahovat číslice.")
            else:
                break
        return last_name

    def get_age(self) -> int:
        # Získání a validace věku pojištěné osoby
        while True:
            try:
                age = int(input("Zadejte věk: ").strip())
                if age >= 0:
                    break
                print("Věk nesmí být záporné číslo.")
            except ValueError:
                print("Zadali jste neplatný věk. Věk musí být celé číslo.")
        return age

    def get_phone_number(self) -> str:
        # Získání a validace formátu telefonního čísla
        while True:
            phone_number = input('Zadejte telefonní číslo: ').strip()
            if (re.search('^(\\+420)? ?[1-9][0-9]{2} ?[0-9]{3} ?[0-9]{3}$', phone_number) != None):
                break
            print('Telefonní číslo je ve špatném formátu.')
        return phone_number


# hlavní třída řídící běh aplikace a interakci mezi jednotlivými komponentami
class Insurance:
    def __init__(self, registry: InsuranceRegistry, form: InsuranceForm) -> None:
        # Inicializace třídy s registrem pojištěnců a formulářem pro zadávání údajů
        self.__registry = registry
        self.__form = form

    def process_request(self) -> None:
        title = '''
--------------------
Evidence pojištěných
--------------------'''

        choice_description = '''
Vyberte jednu z následujících možností:
1. Přidat nového pojištěného
2. Zobrazit seznam pojištěných
3. Vyhledat pojistného pomocí jména a příjmení
4. Konec

'''
        print(title)
        choice = input(choice_description)
        while choice != "4":
            match choice:
                case "1":
                    # Přidání nového pojištěného
                    self.__registry.add_insured_person(
                        InsuredPerson(
                            self.__form.get_first_name(),
                            self.__form.get_last_name(),
                            self.__form.get_age(),
                            self.__form.get_phone_number()
                        )
                    )
                    print("Pojištěný byl úspěšně přidán.")

                case "2":
                    # Zobrazení seznamu všech pojištěných
                    people = self.__registry.list_insured_people()
                    if people:
                        for person in people:
                            print(person)
                    else:
                        print("Žádné pojištěné osoby nejsou evidovány.")

                case "3":
                    # Vyhledání pojištěného podle jména a příjmení
                    first_name = input("Zadejte křestní jméno: ").strip().lower()
                    last_name = input("Zadejte příjmení: ").strip().lower()
                    people = self.__registry.get_insured_person(first_name, last_name)
                    if people:
                        for person in people:
                            print(person)
                    else:
                        print("Pojištěný nebyl nalezen.")

                case _:
                    print('Neplatná volba, zkuste to znovu.')
            # Načtení dalšího vstupu pro další iteraci
            choice = input(choice_description)
        else:
            print("Ukončuji pojišťovací žádost.")


if __name__ == "__main__":
    Insurance(
        InsuranceRegistry(),
        InsuranceForm()
    ).process_request()
