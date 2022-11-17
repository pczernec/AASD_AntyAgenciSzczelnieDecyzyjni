# Agentowe i aktorowe systemy decyzyjne

**Raport A:** Identyfikacja problemu

**Zespół:** AntyAgenci Szczelnie Decyzyjni

**Skład:**

* Wiktor Łazarski
* Rafał Kulus
* Michał Szaknis
* Piotr Czernecki


## Opis problemu

Rozwój internetu i narzędzi do natychmiastowej komunikacji przyspieszył wymianę informacji między ludźmi, niezależnie od ich położenia. W dzisiejszych czasach jesteśmy w stanie przesłać znaczącą ilość informacji do osoby znajdującej się po drugiej stronie świata w mgnieniu oka. *Znacząca ilość informacji* jest tutaj rozumiana jako np. nagranie wideo jakiegoś wydarzenia. Dzięki temu informacje rozprzestrzeniają się w bardzo szybkim tempie. Jesteśmy w stanie dowiedzieć się o różnych wydarzeniach (w szczególności w naszej okolicy), tych pozytywnych jak i negatywnych. Wpływa to na nastrój i samopoczucie osób żyjących w pobliżu miejsc wspomnianych zdarzeń. Szczególnie odbijają się na naszym samopoczuciu wydarzenia negatywne, np. bójki, kradzieże, napaści. Bardzo często odwzorowywane to jest w zmianie pewnych parametrów funkcjonowania naszego organizmu, np. przyspieszone tętno, podniesione ciśnieine. Jednocześnie w dzisiejszym świecie znacząca liczba osób posiada inteligetne zegarki, które potrafią odczytywać różne parametry dotyczące funkcjonowania naszego organizmu. Wiele osób nieświadomie znajduje się w okolicach, w których dochodzi do ww. negatywnych zdarzeń, np. turyści, co uważamy, że jest problemem, który chcielibyśmy rozwiązać przez nas system.


## Propozycja rozwiązania i koncept systemu

**System bezpieczeństwa Twojej lokalizacji**

Przedstawione problemy chcielibyśmy rozwiązać poprzez stworzenie systemu aktorowo-agentowego informującego użytkownika o ocenie jego lokalizacji na mapie z zaznaczonymi obszarami. Agentami naszego systemu byłyby urządzenia monitorujące stan zdrowia człowieka, np. smart watche, które komunikowałyby się ze sobą w celu określania potencjalnych lokalizacji, w których może występować zagrożenie dla człowieka. Odpowiednie dane prezentowane byłyby użytkownikowi w postaci powiadomień na telefon bądź na smart watcha. Dzięki naszemu rozwiązaniu użytkownik może uniknąć miejsc, w których występują bójki uliczne lub manifestacje, podczas których dochodzi do konfliktów, np. Marsz Niepodległości. Działanie systemu polegałoby na komunikacji z agentami znajdującymi się w pobliżu i odpytywaniu ich o "samopoczucie", czyli ocenę stanu użytkownika wyliczaną z danych biometrycznych. Na tej podstawie możliwe będzie wyznaczanie parametrów obszaru stosując np. uśrednianie wartości ze znajdujących się w danej części mapy agentów. Pozwoli to uniknąć komunikacji z centralnym serwerem zbierającym dane od wszystkich użytkowników. Całość można realizować poprzez komunikację jedynie między agentami w danym obszarze. Każdy agent będzie posiadał stan swojego użytkownika do odpowiadania na pytania innych agentów oraz listę z innymi w pobliżu. Celem agenta będzie minimalizowanie czasu spędzanego na obszarach zagrożonych podczas wyznaczania drogi do celu użytkownika. Do rozwiązania określonego zadania można wykorzystać model wielowarstwowy, gdzie poszczególne warstwy mogą być przystosowane do rozwiązywania różnych wariantów problemu. Na przykład przypadek dla małej ilości danych można rozwiązać prostszymi algorytmami, które będą bardziej generalizować dane (np. nie będą niepotrzebnie rozróżniać obszarów o dużej i małej gęstości zebranych informacji).

## Repozytorium

Kod zostanie umieszczony na portalu github.com pod linkiem: https://github.com/pczernec/AASD_AntyAgenciSzczelnieDecyzyjni.git.
