# Render.com-ga Django ERP Tizimini Deploy Qilish

## Render.com nima?
Render.com - bu zamonaviy cloud platformasi bo'lib, web ilovalarni oson va tez deploy qilish imkonini beradi. Heroku-ga o'xshash, lekin yanada arzon va kuchli.

## Kerakli Narsalar

1. **GitHub Account** - Loyihani GitHub-ga yuklash uchun
2. **Render.com Account** - Bepul ro'yxatdan o'tish: https://render.com
3. **Git** - Loyihani GitHub-ga push qilish uchun

## Qadam-ba-qadam Deploy Qilish

### 1. GitHub Repository Yaratish

#### GitHub-da yangi repository yarating:
1. GitHub.com-ga kiring
2. "+" tugmasini bosing va "New repository" tanlang
3. Repository nomi: `django-erp-system` (yoki boshqa nom)
4. Public yoki Private tanlang
5. "Create repository" tugmasini bosing

#### Loyihani GitHub-ga yuklash:
```bash
# Loyiha papkasiga o'ting
cd /Users/umidbek/Downloads/django-erp-system-main

# Git initialize qiling (agar qilinmagan bo'lsa)
git init

# Barcha fayllarni add qiling
git add .

# Commit qiling
git commit -m "Initial commit: Django ERP System"

# GitHub repository-ni remote sifatida qo'shing (URL-ni o'zingizniki bilan almashtiring)
git remote add origin https://github.com/YOUR_USERNAME/django-erp-system.git

# Main branch-ga push qiling
git branch -M main
git push -u origin main
```

### 2. Render.com-da Web Service Yaratish

1. **Render.com-ga kiring**: https://render.com/dashboard
2. **"New +" tugmasini bosing** va **"Web Service"** tanlang
3. **GitHub repository-ni connect qiling**:
   - "Connect account" tugmasini bosing
   - GitHub-ni tanlang va authorize qiling
   - Repository-ni tanlang: `django-erp-system`

### 3. Service Sozlamalari

Quyidagi sozlamalarni kiriting:

#### Asosiy Sozlamalar:
- **Name**: `django-erp-system` (yoki boshqa nom)
- **Region**: `Oregon (US West)` yoki yaqin region
- **Branch**: `main`
- **Runtime**: `Python 3`

#### Build va Start Commands:
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn config.wsgi:application`

#### Pricing:
- **Free Tier** tanlang (boshlanish uchun)

### 4. Environment Variables (Muhim!)

"Environment Variables" bo'limida quyidagi o'zgaruvchilarni qo'shing:

```
SECRET_KEY = django-insecure-your-secret-key-here-make-it-very-long-and-random
DEBUG = False
DJANGO_ALLOWED_HOSTS = your-app-name.onrender.com
DATABASE_URL = postgres://user:password@host:port/database
```

#### SECRET_KEY yaratish:
Terminal-da quyidagi buyruqni bajaring:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. PostgreSQL Database Qo'shish (Ixtiyoriy)

#### Bepul PostgreSQL database yaratish:
1. Render dashboard-da "New +" > "PostgreSQL" tanlang
2. **Name**: `django-erp-db`
3. **Database**: `django_erp`
4. **User**: `django_user`
5. **Region**: Web service bilan bir xil region
6. **Free** plan tanlang

#### Database URL-ni olish:
1. Database yaratilgandan keyin, "Info" tab-ga o'ting
2. "External Database URL" ni ko'chiring
3. Web service-ning Environment Variables-ga `DATABASE_URL` sifatida qo'shing

### 6. Deploy Qilish

1. **"Create Web Service"** tugmasini bosing
2. Render avtomatik ravishda:
   - Repository-ni clone qiladi
   - `build.sh` skriptini ishga tushiradi
   - Dependencies-larni o'rnatadi
   - Database migration-larini bajaradi
   - Static fayllarni to'playdi
   - Aplikatsiyani ishga tushiradi

### 7. Deploy Jarayonini Kuzatish

Deploy logs-da quyidagilarni ko'rasiz:
```
=== Starting build process ===
Installing Python dependencies...
=== Running Django management commands ===
Making migrations...
Running database migrations...
Collecting static files...
=== Creating superuser and employee profile ===
=== Build completed successfully! ===
```

### 8. Aplikatsiyani Ochish

Deploy tugagandan keyin:
1. Service URL-i ko'rsatiladi (masalan: `https://django-erp-system.onrender.com`)
2. Link-ni bosing yoki yangi tab-da oching
3. Django ERP tizimi ishga tushgan bo'ladi!

## Muhim Eslatmalar

### Bepul Plan Cheklovlari:
- **Sleep Mode**: 15 daqiqa faoliyatsizlikdan keyin dastur "uyquga" ketadi
- **Cold Start**: Birinchi so'rov 30-60 soniya davom etishi mumkin
- **750 soat/oy**: Bepul plan uchun cheklangan

### Xavfsizlik:
- **SECRET_KEY**: Hech qachon kodga yozmang
- **DEBUG**: Production-da har doim `False` bo'lishi kerak
- **ALLOWED_HOSTS**: Faqat kerakli domainlarni qo'shing

## Keyingi Deploy-lar

Kodda o'zgarish qilganingizdan keyin:
```bash
git add .
git commit -m "Your changes description"
git push origin main
```

Render avtomatik ravishda yangi deploy-ni boshlaydi.

## Troubleshooting

### Agar deploy muvaffaqiyatsiz bo'lsa:

1. **Logs-ni tekshiring**: Render dashboard-da "Logs" tab
2. **Build muvaffaqiyatsizligi**: `requirements.txt` va `build.sh` ni tekshiring
3. **Database xatolari**: `DATABASE_URL` to'g'riligini tekshiring
4. **Static files**: `ALLOWED_HOSTS` va static files sozlamalarini tekshiring

### Tez-tez uchraydigan xatolar:

**DisallowedHost error**:
```
DJANGO_ALLOWED_HOSTS = your-app-name.onrender.com,localhost,127.0.0.1
```

**Secret key error**:
- `SECRET_KEY` environment variable-ni qo'shing

**Database error**:
- PostgreSQL database yarating va `DATABASE_URL` qo'shing

## Custom Domain (Ixtiyoriy)

O'z domainni qo'shish uchun:
1. Render-da "Settings" > "Custom Domains"
2. Domain nomini qo'shing
3. DNS sozlamalarida CNAME record yarating

## Monitoring

Render dashboard-da:
- **Metrics**: CPU, Memory, Request count
- **Logs**: Real-time logs
- **Activity**: Deploy history

## Maslahatlar

1. **Environment variables** ni GitHub-ga push qilmang
2. **Database backup** ni muntazam qiling
3. **Free plan** test uchun yetarli, production uchun paid plan tavsiya etiladi
4. **SSL** avtomatik ravishda yoqiladi
5. **CDN** static fayllar uchun yoqiladi

## Xulosa

Sizning Django ERP tizimingiz endi Render.com-da ishlaydi! 🎉

- **Tez**: Deploy 5-10 daqiqada tugaydi
- **Bepul**: Boshlanish uchun bepul plan
- **Avtomatik**: Git push qilganingizda avtomatik deploy
- **SSL**: HTTPS avtomatik yoqiladi
- **Scaling**: Kerak bo'lganda osongina scale qilish mumkin
