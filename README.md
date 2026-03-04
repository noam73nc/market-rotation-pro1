# market-rotation-pro1
# 📡 MarketRotation Pro

**דאשבורד אינטראקטיבי לניתוח רוטציה סקטוריאלית בשוק ההון**  
בנוי עם Python + Streamlit | נתונים בזמן אמת מ-Yahoo Finance

---

## מה האפליקציה עושה?

MarketRotation Pro מאפשרת לעקוב אחרי תנועת הכסף בין סקטורים ותעשיות בשוק ההון — ולזהות לאן "מסתובב" הכסף בכל רגע נתון.

### תכונות עיקריות

- **כרטיסי שוק בזמן אמת** — SPY, QQQ, IWM, Dow Jones, Bitcoin, Ethereum, VIX
- **טבלת רוטציה סקטוריאלית** — ביצועים יחסיים ל-SPY על פני 1 שבוע / 1 חודש / 3 חודשים
- **60+ תעשיות ו-ETF** — מוליכים למחצה, AI, קריפטו, אנרגיה, ביוטק, שווקים גלובליים ועוד
- **Scatter Plot אינטראקטיבי** — שינוי מחיר מול נפח מסחר יחסי
- **מצב Dark / Light** — ממשק מותאם לשני מצבי תצוגה

---

## התקנה והרצה מקומית

### דרישות מוקדמות
- Python 3.9 ומעלה
- pip

### שלבים

```bash
# שכפול הפרויקט
git clone https://github.com/YOUR_USERNAME/market-rotation-pro.git
cd market-rotation-pro

# התקנת חבילות
pip install streamlit yfinance pandas numpy

# התקנה אופציונלית (טבלה אינטראקטיבית משופרת)
pip install streamlit-aggrid

# הרצה
streamlit run app_dark_etf.py
```

האפליקציה תיפתח אוטומטית בדפדפן בכתובת: `http://localhost:8501`

---

## הרצה מהירה בענן (ללא התקנה)

> 🔗 **[פתח את האפליקציה ישירות](https://YOUR_APP.streamlit.app)**  
> *(עדכן את הקישור לאחר פריסה ב-Streamlit Cloud)*

---

## חבילות נדרשות

| חבילה | שימוש |
|-------|-------|
| `streamlit` | ממשק המשתמש |
| `yfinance` | נתוני מניות ו-ETF |
| `pandas` | עיבוד נתונים |
| `numpy` | חישובים מתמטיים |
| `streamlit-aggrid` | טבלה אינטראקטיבית (אופציונלי) |

---

## ETFs וסקטורים מכוסים

<details>
<summary>לחץ לרשימה המלאה</summary>

**טכנולוגיה:** SMH, SOXX, IGV, FDN, CIBR, BOTZ, AIQ, QTUM  
**קריפטו:** IBIT, BITO, BLOK, WGMI  
**אנרגיה:** XOP, USO, TAN, FAN, ICLN, URA  
**בריאות:** IBB, XBI, IHI, IHF  
**פיננסים:** KRE, KIE, IAI  
**תעשייה:** ITA, XAR, IYT, JETS  
**סחורות:** GLD, SLV, GDX, COPX, DBA  
**גלובלי:** EEM, FXI, EWZ, INDA, KWEB, **ISRA** 🇮🇱  
**ועוד 20+ קטגוריות נוספות**

</details>

---

## מבנה הפרויקט

```
market-rotation-pro/
│
├── app_dark_etf.py     # קובץ האפליקציה הראשי
└── README.md           # קובץ זה
```

---

## רישיון

פרויקט אישי — חופשי לשימוש אישי ולימודי.  
נתוני שוק מסופקים על ידי Yahoo Finance.

---

*נבנה עם ❤️ ו-Python*
