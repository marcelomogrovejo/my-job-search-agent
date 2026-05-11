# iOS Job Search Agent

Automated agent that scrapes iOS developer job listings from multiple job boards across Vietnam, Japan, Thailand, and international remote platforms, scores them by relevance and location, and sends a formatted HTML email summary on a schedule.

## Job Sources

### Vietnam

| Source | Type | URL | Salary | Posted Date |
|--------|------|-----|--------|-------------|
| ITviec | HTML scraping | [itviec.com](https://itviec.com) | No (login required) | Yes |
| TopDev | HTML scraping | [topdev.vn](https://topdev.vn) | No (login required) | Yes |
| VietnamDevs | HTML scraping | [vietnamdevs.com](https://vietnamdevs.com) | Rarely | Yes |
| ViecLamIT | HTML scraping | [vieclamit.careerviet.vn](https://vieclamit.careerviet.vn) | Yes | No |
| VietnamWorks | REST API | [vietnamworks.com](https://www.vietnamworks.com) | When visible | No |

### Japan

| Source | Type | URL | Salary | Posted Date |
|--------|------|-----|--------|-------------|
| JapanDev | MeiliSearch API | [japan-dev.com](https://japan-dev.com) | Yes (JPY) | Yes |
| TokyoDev | HTML scraping | [tokyodev.com](https://www.tokyodev.com) | Sometimes (JPY) | No |
| Forkwell | HTML scraping | [jobs.forkwell.com](https://jobs.forkwell.com) | Yes (JPY) | Yes (relative) |
| EJable | HTML scraping | [ejable.com](https://www.ejable.com) | No | No |
| GaijinPot | HTML scraping | [jobs.gaijinpot.com](https://jobs.gaijinpot.com) | Yes (JPY) | Yes |

### Thailand

| Source | Type | URL | Salary | Posted Date |
|--------|------|-----|--------|-------------|
| JobsDB | REST API | [th.jobsdb.com](https://th.jobsdb.com) | Sometimes (THB) | Yes |

### Salary considerations
If < $1500 → skip
If $1500–2000 → consider carefully
If $2000+ → strong target

### International

| Source | Type | URL | Salary | Posted Date |
|--------|------|-----|--------|-------------|
| RemoteOK | REST API | [remoteok.com](https://remoteok.com) | No | No |

### Not included — Vietnam

| Platform | Reason |
|----------|--------|
| LinkedIn | Aggressively blocks scraping, requires login, and restricts API access to approved partners. Still the most valuable source — check it manually. |
| Indeed | Minimal presence in Vietnam's tech market. Most listings are aggregated from other sources. Heavy bot detection. |
| Seek | Primarily Australian/NZ. No meaningful Vietnam presence. Their subsidiary JobStreet focuses on Malaysia, Philippines, and Singapore. |

### Not included — Japan

| Platform | Status | Reason |
|----------|--------|--------|
| Indeed Japan | Manual reminder | Cloudflare blocks all non-browser requests. JS-only rendering. robots.txt explicitly disallows scrapers. Large volume but inaccessible. |
| CareerCross | Not added yet | Bilingual job board (EN/JP) for international companies. Has IT category at [careercross.com/en](https://www.careercross.com/en). Worth evaluating. |
| Daijob | Not added yet | Bilingual professional jobs including dev roles at [daijob.com/en](https://www.daijob.com/en). General board, lower tech density. |
| Wantedly | Not added yet | Very popular with Japanese startups at [en-jp.wantedly.com](https://en-jp.wantedly.com). Primarily Japanese-language. Potential rate limiting. |
| HirePlanner | Not added yet | Bilingual IT jobs + career events at [hireplanner.com/en](https://www.hireplanner.com/en). Has dedicated IT section. |
| Findy Global | Not added yet | Developer matching based on GitHub activity at [findy-jobs.io](https://findy-jobs.io). English-facing version available. |

### Not included — Thailand

| Platform | Status | Reason |
|----------|--------|--------|
| Blognone Jobs | Manual reminder | Thailand's top tech-only job board. Cloudflare blocks all requests (HTML and API). Confirmed iOS/Swift listings exist — check manually at [jobs.blognone.com](https://jobs.blognone.com). |
| JobThai | Not added yet | One of Thailand's biggest job sites at [jobthai.com](https://www.jobthai.com/en). Has Mobile Developer subcategory. Thai-primary with English version. |
| WorkVenture | Not added yet | Professional jobs + employer reviews (Thai Glassdoor) at [workventure.com](https://www.workventure.com). Has IT/Programming category. |
| Wellfound | Not added yet | Startup/tech jobs (formerly AngelList) at [wellfound.com](https://wellfound.com/role/l/software-engineer/thailand). English-only, startup-focused. |
| RECRUITdee | Not added yet | IT recruitment agency targeting expat devs in Bangkok at [recruitdee.com](https://www.recruitdee.com). Small but relevant (~20-50 listings). |
| Tech in Asia | Not added yet | SEA tech/startup jobs at [techinasia.com/jobs](https://www.techinasia.com/jobs). Known anti-bot measures. |

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
