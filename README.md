# Assignment 2

## Filer

- `assignment2_analysis.py` — kör alla beräkningar och sparar figurerna
- `build_assignment2_pdf.py` — bygger den färdiga PDF:en
- `Nelson_Plosser_data.xlsx` och `real_gdp_US_2022Q4.xlsx` — datan som används
- `Assignment2_Solutions.pdf` — den färdiga inlämningen

---

## Hur man kör det

Öppna Terminal (Command + Space, skriv "Terminal"), klistra in det här och tryck Enter:

```bash
cd ~/Downloads
uv run --with pandas,numpy,matplotlib,scipy,statsmodels,openpyxl assignment2_analysis.py
uv run --with reportlab build_assignment2_pdf.py
```

Det tar ungefär en minut. När det är klart öppnar du `Assignment2_Solutions.pdf` — det är den du lämnar in.

---

## Om något går fel

**"uv: command not found"** — installera uv härifrån: https://docs.astral.sh/uv/getting-started/installation/

**Skriptet verkar ha fastnat** — det är normalt, Monte Carlo-simuleringen tar upp till 60 sekunder, bara vänta.
