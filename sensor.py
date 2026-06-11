"""
SensorPy – Messdaten analysieren
=================================
Dieses Modul enthält alle Funktionen zur Analyse von Umweltmessdaten.

Aufgabe: Implementiert jede Funktion so, dass sie der Beschreibung
im Docstring entspricht. Die Signatur (Name, Parameter, Rückgabetyp)
darf NICHT verändert werden.

Datenformat (eine Zeile aus messdaten.csv als dict):
    {
        "sensor_id":       "S01",
        "timestamp":       "2024-03-01 08:00",
        "temperatur":      19.2,
        "luftfeuchtigkeit": 52.1,
        "co2":             480.0
    }
"""

import csv

##bs<dlvg<isdvls<dvöiush<dfluiv<sdv
#GROOOOOOOOOOOOOOOOOOOOBER FEHLER
#GRRRR Böse


# ──────────────────────────────────────────────────────────────
# PERSON A grober fehler
# ──────────────────────────────────────────────────────────────

def load_data(filename: str) -> list[dict]:
    """Liest eine CSV-Datei mit Messdaten ein und gibt sie als Liste zurück.

    Jede Zeile der CSV wird in ein dict umgewandelt.
    Numerische Felder (temperatur, luftfeuchtigkeit, co2) werden
    automatisch in float konvertiert.

    Args:
        filename: Pfad zur CSV-Datei (z. B. "data/messdaten.csv")

    Returns:
        Liste von dicts, eines pro Zeile. Leere Liste bei Fehler.

    Beispiel:
        >>> daten = load_data("data/messdaten.csv")
        >>> print(daten[0]["sensor_id"])
        S01
        >>> print(daten[0]["temperatur"])
        19.2
    """
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                entry = dict(row)
                for key in ("temperatur", "luftfeuchtigkeit", "co2"):
                    if key in entry and entry[key] != "":
                        entry[key] = float(entry[key])
                data.append(entry)
            return data
    except (OSError, ValueError):
        return []


def calculate_average(values: list[float]) -> float:
    """Berechnet den Durchschnitt einer Liste von Zahlen.

    Args:
        values: Liste mit float-Werten (darf nicht leer sein)

    Returns:
        Arithmetisches Mittel aller Werte, gerundet auf 2 Dezimalstellen.

    Beispiel:
        >>> calculate_average([10.0, 20.0, 30.0])
        20.0
        >>> calculate_average([19.2, 21.4, 24.7])
        21.77
    """
    return round(sum(values) / len(values), 2)


def find_extremes(values: list[float]) -> tuple[float, float]:
    """Findet den kleinsten und grössten Wert einer Liste.

    Args:
        values: Liste mit float-Werten (darf nicht leer sein)

    Returns:
        Tupel (minimum, maximum)

    Beispiel:
        >>> find_extremes([19.2, 21.4, 24.7, 17.5])
        (17.5, 24.7)
    """
    return (min(values), max(values))


def count_above_threshold(values: list[float], threshold: float) -> int:
    """Zählt, wie viele Werte in der Liste den Schwellenwert überschreiten.

    Args:
        values:    Liste mit float-Werten
        threshold: Schwellenwert (Werte > threshold werden gezählt)

    Returns:
        Anzahl der Werte, die strikt grösser als threshold sind.

    Beispiel:
        >>> count_above_threshold([19.2, 27.1, 24.7, 33.2, 21.4], 25.0)
        2
    """
    return sum(1 for value in values if value > threshold)


# ──────────────────────────────────────────────────────────────
# PERSON B
# ──────────────────────────────────────────────────────────────

def classify_value(value: float, limits: dict) -> str:
    if value < limits["niedrig"]:
        return "niedrig"
    if value < limits["normal"]:
        return "normal"
    if value < limits["hoch"]:
        return "hoch"
    return "kritisch"


def filter_by_sensor(data: list[dict], sensor_id: str) -> list[dict]:
    return [entry for entry in data if entry.get("sensor_id") == sensor_id]


def generate_report(data: list[dict]) -> str:
    if not data:
        return (
            "========== SensorPy Bericht ==========\n"
            "Messungen total:       0\n"
            "Sensoren:              \n\n"
            "-- Temperatur (°C) --\n"
            "Durchschnitt:          0.00\n"
            "Min / Max:             0.0 / 0.0\n"
            "Kritische Werte (>30): 0\n\n"
            "-- Luftfeuchtigkeit (%) --\n"
            "Durchschnitt:          0.00\n"
            "Min / Max:             0.0 / 0.0\n\n"
            "-- CO2 (ppm) --\n"
            "Durchschnitt:          0.00\n"
            "Min / Max:             0.0 / 0.0\n"
            "======================================"
        )

    temperaturen = [entry["temperatur"] for entry in data]
    luftfeuchtigkeit = [entry["luftfeuchtigkeit"] for entry in data]
    co2 = [entry["co2"] for entry in data]
    sensor_ids = sorted({entry["sensor_id"] for entry in data})

    temp_min, temp_max = find_extremes(temperaturen)
    hum_min, hum_max = find_extremes(luftfeuchtigkeit)
    co2_min, co2_max = find_extremes(co2)

    return (
        "========== SensorPy Bericht ==========\n"
        f"Messungen total:       {len(data)}\n"
        f"Sensoren:              {', '.join(sensor_ids)}\n\n"
        "-- Temperatur (°C) --\n"
        f"Durchschnitt:          {calculate_average(temperaturen):.2f}\n"
        f"Min / Max:             {temp_min} / {temp_max}\n"
        f"Kritische Werte (>30): {count_above_threshold(temperaturen, 30.0)}\n\n"
        "-- Luftfeuchtigkeit (%) --\n"
        f"Durchschnitt:          {calculate_average(luftfeuchtigkeit):.2f}\n"
        f"Min / Max:             {hum_min} / {hum_max}\n\n"
        "-- CO2 (ppm) --\n"
        f"Durchschnitt:          {calculate_average(co2):.2f}\n"
        f"Min / Max:             {co2_min} / {co2_max}\n"
        "======================================"
    )
    pass

