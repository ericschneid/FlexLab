# Annahmen und Parameter

Stand: 02.10.2026. Alles mit "offen" ist noch nicht entschieden oder recherchiert.

## 1. Nutzereingaben (nicht fix, in der Oberfläche wählbar)

Jede Eingabe hat Standardwert und Wertebereich (offen, werden mit Quelle und Datum eingetragen).

### Standort
- Ortsname oder Koordinaten (Geocoding)

### Anlage (immer aktiv)
- Beliebig viele Dachflächen, je mit: kWp, Himmelsrichtung (intern Azimut in Grad), Neigung in Grad
- Ein gemeinsamer Wechselrichter: Nennleistung, Wirkungsgrad
- Systemverluste in Prozent (Standardwert offen, PVGIS-Vorgabe prüfen)
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
- Ertrag: nur Standort und Anlage (je Dachfläche kWp, Ausrichtung, Neigung; Systemverluste und Wechselrichter mit Standardwerten)
- Eigenverbrauch und Autarkie: zusätzlich Verbrauch
- Netzbezugskosten: zusätzlich Verbrauch und Stromtarif
- Einspeiseerlöse: Einspeisemodell
- Ersparnis: Netzbezugskosten und Einspeiseerlöse. Referenz ist der Haushalt ohne PV. Der Zusatznutzen jedes weiteren Moduls wird gegen den Zustand ohne dieses Modul ausgewiesen.
- Amortisation: zusätzlich Ersparnis und Anlagenkosten
- Fehlt eine Angabe, werden nur die abhängigen Ergebnisse nicht berechnet. Die Oberfläche nennt den Grund ("nicht berechenbar, weil X fehlt").

## 3. Feste Modellannahmen

### Zeit
- Zeitauflösung: stündlich, alle Zeitreihen auf gleiche Auflösung und Zeitzone

### Ertrag
- Ortsspezifisch aus PVGIS-Wetterdaten und pvlib-Anlagenmodell
- Kein festes Basisjahr. Ausgewiesen werden ein erwarteter Jahresertrag aus einem typischen Wetterjahr und eine Spanne aus mehreren historischen Jahren (gleiche Anlage, jedes Jahr einzeln gerechnet)
- Ein einzelnes kommendes Jahr wird nicht prognostiziert, das Wetter ist nicht vorhersagbar
- Der ERAA-PV-Datensatz wird nicht verwendet: Er ist je Gebotszone aggregiert (DE_LU) und nicht ortsspezifisch

### Preise
- Der Börsenpreis ist nur ein Teil des Haushaltspreises. Netzentgelte, Steuern und Aufschläge sind Nutzereingaben.
- Beim fixen Tarif gibt der Nutzer den Preis selbst ein, es wird keine Preiszeitreihe benötigt. Nur beim