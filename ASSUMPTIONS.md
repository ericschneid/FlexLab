# Annahmen und Parameter

Stand: 03.10.2026. Alles mit "offen" ist noch nicht entschieden oder recherchiert.

## 1. Nutzereingaben (nicht fix, in der Oberfläche wählbar)

Jede Eingabe hat Standardwert und Wertebereich (offen, werden mit Quelle und Datum eingetragen).

### Standort
- Ortsname oder Koordinaten (Geocoding)

### Anlage (immer aktiv)
- Beliebig viele Dachflächen. Pflichtangaben je Dachfläche: kWp und Neigung in Grad. Die Ausrichtung (Himmelsrichtung, intern Azimut in Grad, 180 = Süd) ist optional, Standard ist Süd.
- Ein gemeinsamer Wechselrichter: Nennleistung (Standard: Gesamt-kWp), Wirkungsgrad
- Systemverluste in Prozent (Standardwert ist ein Platzhalter, siehe Abschnitt 3)
- Kein separater Modulwirkungsgrad, die kWp-Angabe enthält ihn

### Module mit Schalter (aus = nicht berücksichtigt, an = Nachfragefelder)
- Anlagenkosten: Investitionskosten der Anlage
- Verbrauch: Jahresverbrauch in kWh, Lastprofil zur Auswahl
- Stromtarif: fix (ct/kWh) oder dynamisch (Day-ahead-Preis plus Aufschläge für Netzentgelte, Steuern, Umlagen als Eingabe)
- Einspeisung: fixe Vergütung oder Börsenpreis (mit Abschlag/Gebühr als Eingabe)
- Batterie: kWh, Leistung in kW, Wirkungsgrad (Standardwerte für Leistung und Wirkungsgrad offen)

### Später
- Demand Side Response, E-Auto, Wärmepumpe, je mit mehreren wählbaren Standardlastprofilen
- Selbstveräußerung des erzeugten Stroms
- Ost-West-Anlage als zwei Dachflächen mit je eigenem Winkel (mit mehreren Dachflächen bereits abbildbar)

## 2. Abhängigkeiten (was braucht was)
- Ertrag: nur Standort und Anlage (je Dachfläche kWp, Neigung, Ausrichtung; Systemverluste und Wechselrichter mit Standardwerten)
- Eigenverbrauch und Autarkie: zusätzlich Verbrauch
- Netzbezugskosten: zusätzlich Verbrauch und Stromtarif
- Einspeiseerlöse: Einspeisemodell
- Ersparnis: Netzbezugskosten und Einspeiseerlöse. Referenz ist der Haushalt ohne PV. Der Zusatznutzen jedes weiteren Moduls wird gegen den Zustand ohne dieses Modul ausgewiesen.
- Amortisation: zusätzlich Ersparnis und Anlagenkosten
- Fehlt eine Angabe, werden nur die abhängigen Ergebnisse nicht berechnet. Die Oberfläche nennt den Grund ("nicht berechenbar, weil X fehlt").

## 3. Feste Modellannahmen

### Zeit und Daten
- Zeitauflösung: stündlich, alle Zeitreihen auf gleiche Auflösung und Zeitzone
- Wetterdaten (PVGIS-TMY) liegen in UTC. Geprüft am 21.06.: Die Einstrahlung beginnt 04:00 und endet 19:00 UTC, symmetrisch um den Sonnenhöchststand.
- Wetterdaten werden in ein Referenzjahr (2001, 8760 Stunden) gelegt, der 29. Februar entfällt
- Umstellung auf deutsche Ortszeit erst beim Zusammenführen mit Verbrauch und Preisen (offen)
- Ortsname zu Koordinaten über OpenStreetMap Nominatim, Wetterdaten werden je Ort lokal zwischengespeichert

### Ertrag
- Ortsspezifisch aus PVGIS-Wetterdaten (typisches Jahr) und pvlib
- Modell: PVWatts-Ansatz je Dachfläche, Summe über alle Flächen, gemeinsamer Wechselrichter
- Kein festes Basisjahr. Ausgewiesen werden ein erwarteter Jahresertrag aus dem typischen Wetterjahr und eine Spanne aus mehreren historischen Jahren (gleiche Anlage, jedes Jahr einzeln gerechnet). Die Spanne ist noch nicht umgesetzt.
- Ein einzelnes kommendes Jahr wird nicht prognostiziert, das Wetter ist nicht vorhersagbar
- Der ERAA-PV-Datensatz wird nicht verwendet: Er ist je Gebotszone aggregiert (DE_LU) und nicht ortsspezifisch
- Platzhalter (noch zu belegen): Systemverluste 10 Prozent, Wechselrichter-Wirkungsgrad 96 Prozent, Leistungstemperaturkoeffizient -0,4 Prozent pro Kelvin, Zelltemperaturmodell SAPM (Glas-Glas, Dachmontage)
- Vereinfachungen: isotropes Himmelsmodell, keine Verschattung, keine Reflexionsverluste, Sonnenstand zur vollen Stunde
- Das typische Jahr setzt sich aus Monaten verschiedener Jahre zusammen. Einzelne Monate können daher unregelmäßig sein (z. B. niedriger August).

### Preise
- Der Börsenpreis ist nur ein Teil des Haushaltspreises. Netzentgelte, Steuern und Aufschläge sind Nutzereingaben.
- Beim fixen Tarif gibt der Nutzer den Preis selbst ein, es wird keine Preiszeitreihe benötigt. Nur beim dynamischen Tarif und bei Börseneinspeisung wird eine Zeitreihe benötigt.
- Zukunft wird über Szenarioparameter abgebildet, nicht über Zeitreihen aus der Zukunft: Die Zeitreihe liefert die Form (Tagesverlauf, Schwankung), das Preisniveau stellt der Nutzer über ein Szenario ein (Mittelwert in ct/kWh oder Faktor auf die Zeitreihe: offen).
- Preisquelle: eigene Eingabe oder ERAA-Szenario (DE_LU). Offen: ERAA-Ausgabe und Zieljahre, Nutzungsbedingungen von ENTSO-E, reale oder nominale Preisbasis.
- Preise sind Szenarien, keine Prognosen. ERAA-Preise stammen aus einer Versorgungssicherheitsstudie, ihre Belastbarkeit ist eine Annahme.

### Verbrauch
- Lastprofil zur Auswahl (BDEW H0 als Grundlage)
- BDEW-Standardlastprofile unterscheiden meines Wissens nicht nach Haushaltstyp (zu prüfen). Varianten wie "berufstätig, tagsüber abwesend" und "Familie, tagsüber zuhause" brauchen eine andere Quelle (z. B. HTW-Berlin-Haushaltsprofile oder synthetische Generatoren, Eignung und Lizenz offen) oder sind selbst gebaute Varianten von H0. Selbst gebaute Varianten sind eigene Annahmen und werden hier einzeln dokumentiert.
- Quellen für E-Auto- und Wärmepumpenprofile: offen

### Vergütung
- Bezug (fix oder dynamisch) und Einspeisung (fest oder Börse) werden unabhängig gewählt, ergibt vier Kombinationen
- Regeln für kleine Anlagen bei Börseneinspeisung ändern sich. Abschlag oder Gebühr ist deshalb Eingabe. Aktuelle Regeln vor Festlegung der Standardwerte prüfen (offen).

## 4. Bekannte Grenzen
- Wetterjahr und Preisjahr sind nicht gekoppelt. Sonnenstunden haben tendenziell niedrige Preise, ohne Kopplung ist der Wert des Eigenverbrauchs, der dynamische Tarif und später DSR verzerrt. Kopplung nur möglich, wenn für dasselbe Klimajahr wie in ERAA stündliche Wetterdaten für den Ort vorliegen (Abdeckung durch PVGIS offen).
- Mehr PV im Netz verändert künftig die Preisform. Ein historisches Preismuster bildet das nicht ab.
- Priorität der Module bei konkurrierendem PV-Überschuss (Batterie, DSR, E-Auto, Wärmepumpe) ist noch nicht festgelegt und beeinflusst die Ergebnisse.
- Verschattung und Reflexionsverluste fehlen, der Ertrag kann dadurch überschätzt sein.
- Typisches Jahr: Monatswerte können unregelmäßig sein, die Jahressumme ist die belastbarere Größe.

## 5. Ergebnisgrößen
- Jahresertrag (erwartet, mit Spanne; Monats- und Tagesverlauf)
- Eigenverbrauchsquote, Autarkiegrad
- Netzbezugskosten, Einspeiseerlöse, Stromkosten mit und ohne Anlage
- Ersparnis, Amortisation

## 6. Zwischenergebnis (noch nicht validiert)
- Laumersheim, 4 kWp, 30 Grad, Süd, Platzhalterwerte: 4421 kWh im Jahr, 1105 kWh pro kWp, Spitzenleistung 3,19 kW
- Globalstrahlung des typischen Jahres: 1248 kWh pro Quadratmeter
- Validierung gegen das PVGIS-Webtool steht aus

## 7. Offene Punkte
- Vergleich mit dem PVGIS-Webtool (Jahresertrag, Monatswerte, Systemverluste). Azimut-Konvention im Tool: 180 = Süd, wie in pvlib. Erster Vergleich (Nordanlage, 30 Grad): PVGIS 2579 kWh.
- Zeitstempel in PVGIS: Momentanwert oder Stundenmittel (Effekt auf den Sonnenstand)
- Standardwerte für Preise, Aufschläge, Anlagenkosten, Systemverluste, Wechselrichter, Batterie (mit Quelle und Datum)
- Preisniveau: Mittelwert oder Faktor
- ERAA: Ausgabe, Zieljahre, Nutzungsbedingungen, Preisbasis
- Quellen für Lastprofile nach Haushaltstyp, E-Auto, Wärmepumpe
- Priorität der Module bei konkurrierendem Überschuss
- Umstellung der Zeitreihen auf Ortszeit
- Betreuer fragen, ob Code, PowerACE oder Institutsdaten aus der Bachelorarbeit verwendet werden dürfen

## 8. Quellen der Standardwerte
| Wert | Standard | Quelle | Datum |
|------|----------|--------|-------|
| Systemverluste | 10 Prozent | keine (Platzhalter) | 03.10.2026 |
| Wechselrichter-Wirkungsgrad | 96 Prozent | keine (Platzhalter) | 03.10.2026 |
| Leistungstemperaturkoeffizient | -0,4 Prozent pro Kelvin | keine (Platzhalter) | 03.10.2026 |