# Agentowe i aktorowe systemy decyzyjne

**Raport B**

**Zespół:** AntyAgenci Szczelnie Decyzyjni

**Skład:**

* Wiktor Łazarski
* Rafał Kulus
* Michał Szaknis
* Piotr Czernecki

## Wymagania funkcjonalne

* Powiadomienie użytkownika o zagrożeniu na podstawie stanu jego i innych użytkowników w jego pobliżu.

## Wymagania niefunkcjonalne

* Działająca sieć urządzeń komunikujących się z innymi urządzeniami w okolicy (Peer-to-Peer).
* Stabilność i działanie systemu niezależne od polityki oszczędzania energii i wydajności urządzenia użytkownika.
* Zapisywanie stanu mapy zagrożeń na wypadek chwilowego braku urządzeń w celu aproksymacji obecnych zagrożeń.

## Role agentów

Smart watch:

* **State collector** - Odczytywanie (zmiany) stanu użytkownika
* **State broadcaster** - Wysyłanie zanonimizowanego stanu użytkownika do urządzeń w okolicy
* **State receiver** - Nasłuchiwanie na informacje o stanie od agentów w okolicy
* **Danger notifier** - Informowanie użytkownika o pobliskim zagrożeniu

## Komunikaty

* **USER STATE** - Stan użytkownika (jego stan zdrowia + lokalizacja, w której się znajduje)
* **ANONYMISED USER STATE** - Zanonimizowany stan użytkownika przeznaczony do wysyłania do innych agentów 
* **ANONYMISED USER STATE BATCH** - Zagregowany stan użytkowników z okolicy

## Scenariusz

1. Rola `State collector` okresowo pobiera informacje z czujników analizujących stan zdrowotny oraz lokalizację użytkownika i, jeśli stan się zmienił, zostaje on przesłany do roli `State broadcaster` w ramach komunikatu `USER STATE`.
2. Rola `State broadcaster` otrzymuje komunikat otrzymany od roli `State collector`. Następnie zapisuje otrzymany komunikat w bazie danych. W kolejnym kroku wiadomość jest przesyłana do roli `Danger notifier`, a jej zanonimizowana wersja jest rozgłaszana do innych agentów jako komunikat typu `ANONYMISED USER STATE`.
3. Jednocześnie, agent rozgłaszający wiadomość nasłuchuje w ramach roli `State receiver` na wiadomości rozgłaszane przez inne agenty. Rola ta agreguje odebrane komunikaty i okresowo sprawdza, czy stan agregacji się zmienił, a jeśli tak, przekazuje je do roli `Danger notifier` w ramach komunikatu `ANONYMISED USER STATE BATCH`. 
4. Rola `Danger notifier` po otrzymaniu komunikatu `USER STATE` (od roli `State broadcaster`) lub `ANONYMISED USER STATE BATCH` (od roli `State collector`) oblicza na podstawie otrzymanych i historycznych danych nowy poziom zagrożenia użytkownika. W przypadku przekroczenia wartości krytycznej, użytkownik jest powiadamiany o prawdopodobnym zagrożeniu w jego okolicy.

<div style="page-break-after: always; break-after: page;"></div>

## Schemat systemu

![diagram](https://raw.githubusercontent.com/pczernec/AASD_AntyAgenciSzczelnieDecyzyjni/main/diagrams/diagram.svg)
