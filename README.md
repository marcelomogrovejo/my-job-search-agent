# iOS Job Search Agent

Automated agent that scrapes iOS developer job listings from multiple Vietnamese and international job boards, scores them by relevance and location, and sends a formatted HTML email summary on a schedule.

## Job Sources

### Vietnam

| Source | Type | URL | Salary | Posted Date |
|--------|------|-----|--------|-------------|
| ITviec | HTML scraping | [itviec.com](https://itviec.com) | No (login required) | Yes |
| TopDev | HTML scraping | [topdev.vn](https://topdev.vn) | No (login required) | Yes |
| VietnamDevs | HTML scraping | [vietnamdevs.com](https://vietnamdevs.com) | Rarely | Yes |
| ViecLamIT | HTML scraping | [vieclamit.careerviet.vn](https://vieclamit.careerviet.vn) | Yes | No |
| VietnamWorks | REST API | [vietnamworks.com](https://www.vietnamworks.com) | When visible | No |

### International

| Source | Type | URL | Salary | Posted Date |
|--------|------|-----|--------|-------------|
| RemoteOK | REST API | [remoteok.com](https://remoteok.com) | No | No |

### Not included

| Platform | Reason |
|----------|--------|
| LinkedIn | Aggressively blocks scraping, requires login, and restricts API access to approved partners. Still the most valuable source — check it manually. |
| Indeed | Minimal presence in Vietnam's tech market. Most listings are aggregated from other sources. Heavy bot detection. |
| Seek | Primarily Australian/NZ. No meaningful Vietnam presence. Their subsidiary JobStreet focuses on Malaysia, Philippines, and Singapore. |

## Setup

### Requirements

```
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file or set these as GitHub Secrets:

```
EMAIL_USER=your-email@gmail.com
EMAIL_APP_PASSWORD=your-gmail-app-password
EMAIL_TO=recipient@example.com
```

### Run Locally

```
python main.py
```

### GitHub Actions

The workflow runs automatically on **Monday and Thursday at 22:00 UTC** via `.github/workflows/daily.yml`. It can also be triggered manually from the Actions tab.
