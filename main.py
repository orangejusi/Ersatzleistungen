import random as random
import threading


# Zinsen hinzufügen
def loop():
    threading.Timer(300, loop).start()
    with open('benutzer.txt', encoding='utf-8') as file:
        data = file.readlines()
        for u, f in enumerate(data):
            data[u] = f"{f.split('/')[0]}/{f.split('/')[1]}" \
                      f"/{round(float(f.split('/')[2]) * 1.035, 2)}/{f.split('/')[3]}"

    with open('benutzer.txt', 'w', encoding='utf-8') as file:
        file.writelines(data)


loop()


# Konto erstellen
class Konto:
    def __init__(self, inhaber, kontonummer, kontostand, pini):
        self.inhaber = inhaber
        self.kontonummer = int(kontonummer)
        self.kontostand = float(kontostand)
        self.pin = pini

    def inhaber(self):
        return self.inhaber()

    def ueberweisen(self, ziel, betrag, kn):
        if self.kontostand - betrag >= 0:
            with open('benutzer.txt', encoding='utf-8') as file:
                data = file.readlines()
                for u, f in enumerate(data):
                    if str(f.split('/')[0].lower().strip()) == str(ziel.lower().strip()):
                        data[u] = f"{f.split('/')[0]}/{f.split('/')[1]}/" \
                                  f"{float(f.split('/')[2]) + float(betrag)}/{f.split('/')[3]}"
                        break
                else:
                    print("Ziel wurde nicht gefunden!")
                    return

            with open('benutzer.txt', 'w', encoding='utf-8') as file:
                file.writelines(data)

            self.kontostand -= float(betrag)
            with open('benutzer.txt', encoding='utf-8') as file:
                data = file.readlines()
                for u, f in enumerate(data):
                    if f.split('/')[1] == kn:
                        data[u] = f"{f.split('/')[0]}/{f.split('/')[1]}/" \
                                  f"{float(f.split('/')[2]) - float(betrag)}/{f.split('/')[3]}"
                        break

            with open('benutzer.txt', 'w', encoding='utf-8') as file:
                file.writelines(data)

            print("Erfolgreiche Überweisung! Neuer Kontostand: " + str(self.kontostand))
        else:
            print("Keine Deckung vorhanden!")

    def einzahlen(self, betrag, kn):
        self.kontostand += float(betrag)
        with open('benutzer.txt', encoding='utf-8') as file:
            data = file.readlines()
            for u, f in enumerate(data):
                if f.split('/')[1] == kn:
                    data[u] = f"{f.split('/')[0]}/{f.split('/')[1]}" \
                              f"/{float(f.split('/')[2]) + float(betrag)}/{f.split('/')[3]}"

        with open('benutzer.txt', 'w', encoding='utf-8') as file:
            file.writelines(data)

        print("Neuer Kontostand: " + str(self.kontostand))

    def auszahlen(self, betrag, kn):
        if self.kontostand >= float(betrag):
            with open('benutzer.txt', encoding='utf-8') as file:
                data = file.readlines()
                for u, f in enumerate(data):
                    if f.split('/')[1] == kn:
                        data[u] = f"{f.split('/')[0]}/{f.split('/')[1]}/{float(f.split('/')[2]) - float(betrag)}" \
                                  f"/{f.split('/')[3]}"

            with open('benutzer.txt', 'w', encoding='utf-8') as file:
                file.writelines(data)
            self.kontostand -= float(betrag)
            print("Neuer Kontostand: " + str(self.kontostand))
        else:
            print("Nicht genügend Deckung vorhanden.")


def op(kontonum):
    operation = input(
        "\nWas möchten Sie tun? Eine Überweisung tätigen, eine Einzahlung tätigen, eine Auszahlung tätigen "
        "oder das "
        "Programm verlassen?\n").lower()

    if operation == "einzahlung":
        mein_konto.einzahlen(input("Wie viel möchten Sie einzahlen: "), kontonum)

    elif operation == "auszahlung":
        mein_konto.auszahlen(input("Wie viel möchten sie abheben: "), kontonum)

    elif operation == "kontostand":
        print("Aktueller Kontostand:" + str(mein_konto.kontostand), kontonum)

    elif operation == "überweisung":
        mein_konto.ueberweisen(input("An wen möchtest du überweisen: "), float(input("Wie viel möchtest du "
                                                                                     "überweisen: ")), kontonum)

    elif operation == "verlassen":
        print("Vielen Dank für Ihre Benutzung\n")
        return


while True:
    # Konto erstellen oder anmelden
    if input("Möchten Sie sich anmelden oder ein Konto erstellen? \n").lower() == "erstellen":
        mein_konto = Konto(input("Name:"), int(random.randint(100000000, 999999999)), 1000,
                           int(input("Bitte geben Sie Ihre selbst gewählte Pin ein: ")))

        with open('benutzer.txt', 'a') as line:
            line.write(
                f"\n{mein_konto.inhaber}/{mein_konto.kontonummer}/{float(mein_konto.kontostand)}/{mein_konto.pin}")

    else:
        benutzer = input("Bitte geben Sie Ihren Namen ein: ")

        with open('benutzer.txt') as line:
            for s in line:
                # Instanz erstellen mit Daten aus benutzer.txt
                mein_konto = Konto(s.split('/')[0], s.split('/')[1], float(s.split('/')[2]), s.split('/')[3])

                # Falls Benutzer existiert
                if benutzer == mein_konto.inhaber:
                    i = 3
                    # Versuche
                    while i > 0:
                        pin = input("Bitte geben Sie Ihren PIN ein! " + str(i) + "/3 Versuche: ")
                        if pin == mein_konto.pin:
                            while True:
                                op(s.split('/')[1])
                                exit()
                        else:
                            if i > 1:
                                i -= 1
                                print("Die PIN ist falsch! Bitte erneut versuchen!")
                            else:
                                break

                    print("Die PIN ist falsch! Sie haben keine Versuche mehr. Bruh.")
                    exit()
            else:
                print("Ihr Benutzername konnte nicht gefunden werden!")
