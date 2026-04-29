# 🏥 Polyclinic Management System — ER Diagram

Bu diagramma **MySQL 8** bazasi uchun loyihalashtirilgan. Mermaid formatida — GitHub, VS Code (Markdown Preview) va dbdiagram.io'da ko'rsa bo'ladi.

## ER Diagram

```mermaid
erDiagram
    DISCOUNT_CATEGORY ||--o{ PATIENT : "beriladi"
    PATIENT ||--o{ VISIT : "qiladi"
    DOCTOR ||--o{ VISIT : "qabul qiladi"
    SPECIALTY ||--o{ DOCTOR : "egallaydi"
    QUALIFICATION ||--o{ DOCTOR : "darajasi"
    VISIT ||--o{ VISIT_PROCEDURE : "ichida"
    PROCEDURE_TYPE ||--o{ VISIT_PROCEDURE : "qo'shiladi"
    VISIT ||--o{ VISIT_CONSULTATION : "ichida"
    DOCTOR ||--o{ VISIT_CONSULTATION : "konsultatsiya beradi"
    VISIT ||--o| PAYMENT : "to'lanadi"

    DISCOUNT_CATEGORY {
        int id PK
        varchar name "Nafaqaxor, Faxriy, Bola..."
        decimal percent "0.00 - 100.00"
        text description
        boolean is_active
    }

    PATIENT {
        int id PK
        varchar full_name
        date birth_date
        enum gender "M, F"
        varchar phone UK
        varchar address
        int discount_category_id FK
        datetime created_at
        datetime updated_at
    }

    SPECIALTY {
        int id PK
        varchar name UK "Kardiologiya, Terapiya..."
        text description
    }

    QUALIFICATION {
        int id PK
        varchar name UK "Oliy, Birinchi, Ikkinchi..."
        decimal price_multiplier "narx koeffitsienti"
    }

    DOCTOR {
        int id PK
        varchar full_name
        int specialty_id FK
        int qualification_id FK
        decimal consultation_price
        varchar phone
        boolean is_active
        datetime created_at
    }

    PROCEDURE_TYPE {
        int id PK
        varchar name "UZI, Qon tahlili..."
        decimal base_price
        int duration_minutes
        text description
        boolean is_active
    }

    VISIT {
        int id PK
        int patient_id FK
        int primary_doctor_id FK
        date visit_date
        text diagnosis
        decimal subtotal "chegirmagacha"
        decimal discount_amount
        decimal total_cost "yakuniy"
        enum payment_status "PENDING, PAID, CANCELLED"
        datetime created_at
        datetime updated_at
    }

    VISIT_PROCEDURE {
        int id PK
        int visit_id FK
        int procedure_type_id FK
        decimal price_at_time "tarix uchun"
        int quantity
        text notes
    }

    VISIT_CONSULTATION {
        int id PK
        int visit_id FK
        int doctor_id FK
        decimal price_at_time
        text notes
    }

    PAYMENT {
        int id PK
        int visit_id FK UK
        decimal amount
        enum method "CASH, CARD, TRANSFER"
        datetime paid_at
        varchar receipt_number
    }
```

---

## 🧩 Bog'lanishlarning izohi (Cardinality)

| Bog'lanish | Tip | Tushuntirish |
|------------|-----|--------------|
| `DISCOUNT_CATEGORY` → `PATIENT` | 1 : N | Bir chegirma toifasiga *ko'p* bemor |
| `PATIENT` → `VISIT` | 1 : N | Bir bemorda *ko'p* murojaat |
| `DOCTOR` → `VISIT` | 1 : N | Bir shifokor *ko'p* bemorni qabul qiladi |
| `SPECIALTY` → `DOCTOR` | 1 : N | Bir mutaxassislikda *ko'p* shifokor |
| `QUALIFICATION` → `DOCTOR` | 1 : N | Bir kategoriyada *ko'p* shifokor |
| `VISIT` ↔ `PROCEDURE_TYPE` | M : N | Murojaat = ko'p protsedura, protsedura = ko'p murojaat → `VISIT_PROCEDURE` |
| `VISIT` ↔ `DOCTOR` (konsultatsiya) | M : N | → `VISIT_CONSULTATION` |
| `VISIT` → `PAYMENT` | 1 : 1 | Bitta murojaatga bitta to'lov |

---

## 📐 Normallashtirish (3NF)

✅ **1NF** — har bir katak atomik (telefon, manzil bo'linmagan)
✅ **2NF** — barcha PK lar yagona (id), kompozit kalitlar yo'q
✅ **3NF** — tranzitiv bog'liqlik yo'q:
- Mutaxassislik `DOCTOR` jadvalida emas, alohida `SPECIALTY` jadvalida
- Chegirma foizi `PATIENT` da emas, `DISCOUNT_CATEGORY` da
- Protsedura nomi va narxi `PROCEDURE_TYPE` da, `VISIT_PROCEDURE` da faqat `price_at_time` (tarixiy narx)

---

## 🔑 Asosiy Biznes-qoidalar (DB darajasida)

1. **`price_at_time`** — protsedura/konsultatsiya narxi *o'zgarishi mumkin*. Murojaat tarixini saqlash uchun shu paytdagi narxni nusxalash.
2. **`subtotal` vs `total_cost`** — chegirmagacha va keyin. Hisobot uchun ikkalasi ham kerak.
3. **`UNIQUE(phone)`** — bemor telefonida dublikat bo'lmasin.
4. **`is_active`** — shifokor/protsedurani o'chirmaymiz, faqat nofaol qilamiz (tarix uchun).
5. **`CASCADE` vs `RESTRICT`** — bemor o'chirilsa murojaatlari ham (CASCADE), ammo shifokorni o'chirib bo'lmaydi agar murojaatlari bo'lsa (RESTRICT).
