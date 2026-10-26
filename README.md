# DACH Gewerbe-Photovoltaik-, ? 3 Nr. 72 EStG (30 kWp) vs. ? 7g IAB/Sonder-AfA- & EEG-Amortisations-Rechner 2026 (`pv-gewerbe-dach`)

Open-Source Python SDK & CLI zur finanzmathematischen und steuerlichen Optimierung gewerblicher Photovoltaik- und Batteriespeicheranlagen in **Deutschland (DE)**, **?sterreich (AT)** und der **Schweiz (CH)**.

?? **Live Web-Applikation & 20-Jahres-Cashflow-Dossier (100 % Client-Side):**
- **[Gewerbe-Photovoltaik-, ? 3 Nr. 72 EStG vs. ? 7g IAB/Sonder-AfA- & EEG-Rechner 2026](https://dachdigitalwerk.github.io/photovoltaik-gewerbe-amortisations-rechner/)**
- **[? 3 Nr. 72 EStG: 30-kWp-Grenze Gewerbe & Einheiten-Multiplikator](https://dachdigitalwerk.github.io/photovoltaik-gewerbe-amortisations-rechner/photovoltaik-steuerfrei-3-nr-72-estg-30-kwp-grenze-gewerbe-2026.html)**
- **[? 7g EStG: 50 % IAB + 40 % Sonder-AfA = 72,5 % Sofortabschreibung](https://dachdigitalwerk.github.io/photovoltaik-gewerbe-amortisations-rechner/pv-anlage-gewerbe-abschreibung-iab-7g-sonder-afa-rechner-2026.html)**
- **[EEG-Einspeiseverg?tung 2026: Leistungsgewichtete Staffelung (? 48 EEG)](https://dachdigitalwerk.github.io/photovoltaik-gewerbe-amortisations-rechner/einspeiseverguetung-2026-eeg-staffelung-teileinspeisung-volleinspeisung-rechner.html)**

## Kernfunktionen

1. **? 3 Nr. 72 EStG Freigrenzen-Pr?fung:** Einheitliche 30,0 kWp Grenze je Wohn-/Gewerbeeinheit (max. 100,0 kWp pro Steuerpflichtigem).
2. **? 7g EStG Abschreibungsturbo (72,5 % bis Ende Jahr 1):** Kombination aus 50 % Investitionsabzugsbetrag (? 7g Abs. 1 EStG), 40 % Sonder-AfA (? 7g Abs. 5 EStG auf 50 % Rest-BMG = 20 %) und 5 % linearer AfA (= 2,5 %).
3. **? 48 EEG Mischsatz-Engine:** Leistungsgewichtete Berechnung f?r Teileinspeisung und Volleinspeisung (10 / 40 / 100 kWp).

## Installation & Schnellstart

```bash
pip install -e .
dach-pv-gewerbe --kwp 85.0 --capex 101000 --tax-rate 0.42 --units 1
```

## Lizenz & Hinweis

MIT License. Keine Steuer- oder Rechtsberatung (? 5 StBerG / ? 2 RDG).
