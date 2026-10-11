# Rima Gemini Image Proxy

یک پراکسی ساده Flask برای دریافت تصویر، ارسال آن به Gemini و برگرداندن پاسخ JSON.

## اجرا و آزمایش محلی

1. Python 3.10 یا جدیدتر نصب کنید.
2. در این پوشه محیط مجازی بسازید و وابستگی‌ها را نصب کنید:

   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. کلید Gemini را در متغیر محیطی قرار دهید (از قراردادن کلید در کد یا مخزن خودداری کنید):

   ```bash
   # macOS/Linux
   export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
   # Windows PowerShell
   $env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
   ```
4. اجرا کنید: `python app.py` و سپس `http://localhost:5000/` را باز کنید.
5. تصویر را با فیلد `image` و در صورت نیاز متن `prompt` به `POST /analyze` بفرستید:

   ```bash
   curl -X POST http://localhost:5000/analyze \
     -F "image=@photo.jpg" \
     -F "prompt=این تصویر را به فارسی توصیف کن"
   ```

پاسخ موفق: `{"result":"..."}`. محدودیت تصویر ۱۵ مگابایت است. متغیر اختیاری `GEMINI_MODEL` برای تغییر مدل وجود دارد؛ مقدار پیش‌فرض `gemini-1.5-flash` است. نام مدل‌های موجود ممکن است با حساب/نسخهٔ API متفاوت باشد.

## استقرار روی Render

1. این پوشه را در یک مخزن Git قرار دهید و به Render متصل کنید.
2. یک **Web Service** بسازید؛ Runtime را Python انتخاب کنید.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. در بخش **Environment** متغیر `GEMINI_API_KEY` را با کلید Gemini اضافه کنید. در صورت نیاز `GEMINI_MODEL` را نیز تنظیم کنید.
6. Deploy کنید؛ آدرس سرویس شما endpointهای `/` و `/analyze` را ارائه می‌دهد.

## استقرار روی PythonAnywhere

1. فایل‌ها را آپلود یا از Git دریافت کنید و در **Web** یک برنامهٔ Flask/Python بسازید.
2. در تب **Web** یک virtualenv تعیین و در کنسول Bash آن را آماده کنید:

   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 rima-proxy
   pip install -r /مسیر/به/rima_proxy_server/requirements.txt
   ```
3. در بخش **Web → Code** مقدار Source code را روی پوشهٔ پروژه بگذارید و فایل WSGI را طوری تنظیم کنید که برنامهٔ Flask را از `app.py` وارد کند؛ برای مثال:

   ```python
   import os, sys
   project = "/home/USERNAME/rima_proxy_server"
   if project not in sys.path:
       sys.path.insert(0, project)
   from app import app as application
   ```
4. کلید را به‌صورت متغیر محیطی `GEMINI_API_KEY` برای برنامه تنظیم کنید (از قراردادن آن در فایل عمومی/مخزن پرهیز کنید)، سپس در تب Web گزینهٔ **Reload** را بزنید.

در نسخهٔ رایگان PythonAnywhere ممکن است دسترسی خروجی به سرویس Gemini محدود باشد؛ پیش از انتخاب این میزبان، دسترسی شبکه و محدودیت‌های حساب را بررسی کنید. کلید Gemini را محرمانه نگه دارید و endpoint را در صورت استفادهٔ عمومی با احراز هویت/محدودیت نرخ محافظت کنید.
