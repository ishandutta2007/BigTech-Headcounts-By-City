# 🤝 Contributing to BigTech Headcounts By City

Thank you for considering contributing to **BigTech Headcounts By City**! Your contributions help keep tech hub headcount estimates accurate, up to date, and valuable for the community.

---

## 🚀 Quick Start Guide

### Project Structure

```
.
├── data/
│   ├── headcounts_2026.json   # Primary dataset for 2026 (USA + India)
│   ├── data_usa_2026.json     # USA regional breakdown
│   └── data_india_2026.json   # India regional breakdown
├── README.md                  # Main project landing page containing tables
└── update_readme.py           # Automation script to regenerate README tables
```

---

## 📊 Updating or Adding Headcount Data

We follow a year-by-year JSON dataset model stored in the `data/` directory.

### 1. Adding Data for a New Year (e.g., 2027)

1. Create a new file in the `data/` folder named `headcounts_YYYY.json` (for example, `data/headcounts_2027.json`).
2. Use the schema structure shown below:

```json
{
  "year": 2027,
  "usa": [
    {
      "region": "San Francisco Bay Area, CA",
      "subtext": "(SF/Silicon Valley)",
      "emoji": "🌉",
      "google": "29,000+",
      "amazon": "8,500+",
      "microsoft": "4,500+",
      "apple": "33,000+",
      "meta": "23,000+",
      "adobe": "7,500+",
      "total": "105,500+"
    }
  ],
  "india": [
    {
      "region": "Bengaluru, KA",
      "subtext": "(Primary R&D)",
      "emoji": "🌆",
      "google": "4,200+",
      "amazon": "7,000+",
      "microsoft": "3,200+",
      "apple": "1,200+",
      "meta": "~150",
      "adobe": "2,800+",
      "total": "18,550+"
    }
  ]
}
```

3. Run the update script from the root directory:

```bash
python update_readme.py
```

The script will automatically detect the newest year (`data/headcounts_YYYY.json`), calculate column & row totals, format the Markdown tables, and update `README.md`.

---

## 🛠️ Modifying the Update Script (`update_readme.py`)

If you want to add new companies, regions, or tweak table formatting:
1. Edit `update_readme.py`.
2. Test your changes locally by running `python update_readme.py`.
3. Check `git diff README.md` to ensure table formatting remains clean and aligned.

---

## 📥 Submitting a Pull Request (PR)

1. **Fork** the repository and create your feature branch:
   ```bash
   git checkout -b feature/update-2027-headcounts
   ```
2. **Commit** your changes with clear messaging:
   ```bash
   git commit -m "feat: add 2027 tech hub headcount estimations"
   ```
3. **Push** to your branch and submit a **Pull Request** detailing the sources or reasoning behind the updated figures.

---

## 💖 Thank You!

Your contributions make this project possible!
