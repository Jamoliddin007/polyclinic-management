# 🏥 Polyclinic Management System

Pullik poliklinikaning rejalashtirish xizmati uchun to'liq web-ilova. Bemorlarni ro'yxatga olish, shifokor murojaatlari, protseduralar, chegirmalar va to'lovlarni boshqaradi.

> **Status:** 🚧 Ishlab chiqilmoqda (Bosqich 1/7)

---

## 📋 Asosiy imkoniyatlar

- 👥 **Bemorlarni boshqarish** — ro'yxatga olish, qidirish, tarix
- 👨‍⚕️ **Shifokorlar va mutaxassisliklar** — kategoriya, narx
- 📅 **Murojaatlar** — tashxis, protseduralar, konsultatsiyalar
- 💰 **Avtomatik narx hisoblash** — chegirma toifalari bilan
- 💳 **To'lovlar** — naqd, karta, o'tkazma
- 📊 **Hisobotlar** — kunlik daromad, eng faol shifokorlar, PDF/Excel eksport
- 🔐 **Rollarga asoslangan kirish** — admin, registrator, shifokor

---

## 🛠 Texnologiyalar

| Qatlam | Texnologiya |
|--------|-------------|
| **Backend** | Python 3.11, Django 5, Django REST Framework |
| **Database** | MySQL 8 |
| **Frontend** | React 18, Vite, TailwindCSS |
| **Auth** | JWT (djangorestframework-simplejwt) |
| **Deploy** | Docker, docker-compose |
| **CI/CD** | GitHub Actions |

---

## 📁 Loyiha tuzilishi

```
polyclinic-management/
├── backend/              # Django + DRF API
│   ├── polyclinic_project/
│   ├── apps/
│   │   ├── patients/
│   │   ├── doctors/
│   │   ├── visits/
│   │   ├── billing/
│   │   └── reports/
│   └── manage.py
├── frontend/             # React + Vite + Tailwind
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/                 # Diagrammalar, schema, qo'llanmalar
│   ├── er-diagram.md
│   ├── class-diagram.md
│   └── database_schema.sql
├── docker/               # Dockerfile va sozlamalar
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Ishga tushirish

### 1. Repozitoriyni klonlash

```bash
git clone https://github.com/<username>/polyclinic-management.git
cd polyclinic-management
```

### 2. MySQL bazasini yaratish

```bash
mysql -u root -p < docs/database_schema.sql
```

### 3. Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate            # Linux/Mac
# venv\Scripts\activate             # Windows
pip install -r ../requirements.txt
cp ../.env.example .env              # va to'ldiring
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend: http://localhost:8000
Admin: http://localhost:8000/admin

### 4. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

### 5. Docker orqali (oson variant)

```bash
docker-compose up --build
```

---

## 📊 Ma'lumotlar bazasi

ER Diagram va schema [`docs/`](docs/) papkasida:

- [`docs/er-diagram.md`](docs/er-diagram.md) — Entity-Relationship diagramma
- [`docs/class-diagram.md`](docs/class-diagram.md) — UML Class va Use Case
- [`docs/database_schema.sql`](docs/database_schema.sql) — MySQL CREATE TABLE skripti

---

## 🗺 Roadmap

- [x] **Bosqich 1:** Loyiha asosi va hujjatlashtirish
- [ ] **Bosqich 2:** ER Diagram va MySQL schema
- [ ] **Bosqich 3:** Django models va admin panel
- [ ] **Bosqich 4:** REST API va biznes-mantiq
- [ ] **Bosqich 5:** React frontend
- [ ] **Bosqich 6:** Hisobotlar va analitika
- [ ] **Bosqich 7:** Testlar, Docker, deploy

---

## 📜 Litsenziya

MIT License — [LICENSE](LICENSE) faylida

---

## 👤 Muallif

UIC Academy talabasi loyihasi.

Savollar uchun: [GitHub Issues](https://github.com/)
