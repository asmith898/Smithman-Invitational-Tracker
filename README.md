# Smithman Invitational League HQ

Free static dashboard for FPL classic league **418812**.

## Publish (free)
1. Create a **public** GitHub repository and upload the contents of this folder (including `.github/workflows/update.yml`).
2. Under **Settings → Actions → General → Workflow permissions**, allow **Read and write permissions** if required for the workflow to commit data.
3. Open **Actions → Update FPL dashboard → Run workflow**. This downloads public FPL data into `data/dashboard.json`.
4. Under **Settings → Pages**, choose **Deploy from a branch**, branch **main**, folder **/(root)**, and save.
5. Your site appears at `https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`. Scheduled updates run hourly (GitHub scheduling may be delayed).

## Local preview
Run `python update.py` (requires internet access), then `python -m http.server 8000` and open `http://localhost:8000`.

## Prize rules and limitations
- Configure amounts in `config.json`. The weekly £1.50 and monthly £4 are split equally for ties.
- Weekly awards are counted only when FPL marks a gameweek finished and data checked.
- **Monthly rule is an assumption:** gameweeks are grouped by calendar month of FPL deadline; monthly award is issued only once all gameweeks in that month are checked. Verify against the Excel workbook's custom month boundaries.
- League winner and runner-up amounts are displayed as projections only. Cup, second-last, highest-week and highest-month special prizes are **not yet calculated**. These need rule verification before implementation.
- Historic 2025/26 data is **not imported**; the records page currently covers current-season FPL history only.
- FPL API is unofficial/undocumented, and may change or throttle requests. GitHub scheduled workflows may be delayed or disabled after inactivity. This is near-live scheduled data, not second-by-second match updates.
- Data is public, including manager names and points. Don't publish private payment details.
