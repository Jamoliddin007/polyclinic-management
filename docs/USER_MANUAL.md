# 📖 Foydalanuvchi qo'llanmasi — Polyclinic Management System

Ushbu qo'llanma poliklinika xodimlari uchun tizimdan foydalanish bo'yicha to'liq ko'rsatma beradi.

---

## 🚪 1. Tizimga kirish

1. Brauzerda http://localhost (yoki sizga berilgan manzilni) oching.
2. Login va parolingizni kiriting.
3. **Kirish** tugmasini bosing.

> 💡 Parolni unutgan bo'lsangiz, admin bilan bog'laning.

---

## 👥 2. Bemorlar bilan ishlash

### 2.1. Bemorni ro'yxatga olish

1. Sidebar'da **👥 Bemorlar** ni tanlang.
2. **+ Yangi bemor** tugmasini bosing.
3. Quyidagi maydonlarni to'ldiring:
   - **F.I.O.** (majburiy)
   - **Tug'ilgan sana** (majburiy)
   - **Jinsi** (majburiy)
   - **Telefon** (majburiy, takrorlanmasligi kerak — `+998 90 123 45 67`)
   - **Manzil** (ixtiyoriy)
   - **Chegirma toifasi** (agar bemor nafaqaxor, faxriy va h.k. bo'lsa)
4. **Saqlash** ni bosing.

### 2.2. Bemorni qidirish

Yuqoridagi qidiruv maydoniga ism, telefon yoki manzil qismi kiriting — natijalar avtomatik filtrlanadi.

### 2.3. Bemor ma'lumotlarini tahrirlash

Bemor qatoridagi **Tahrirlash** tugmasini bosing.

### 2.4. Bemorni o'chirish

⚠️ **Diqqat:** O'chirilsa, bemorning barcha murojaatlari ham o'chiriladi.

---

## 👨‍⚕️ 3. Shifokorlar

Sidebar'da **👨‍⚕️ Shifokorlar**:
- Mutaxassislik bo'yicha filter
- Yakuniy narx avto-hisoblanadi: `consultation_price × qualification_multiplier`
- Faol/nofaol holatini ko'rish

Shifokor narxi formula:
```
Yakuniy narx = Asosiy narx × Malaka koeffitsienti
                100 000  ×  1.5 (Oliy toifa) = 150 000
```

---

## 📅 4. Murojaat yaratish (eng muhim oqim)

### Qadam 1: Asosiy ma'lumotlar
1. **📅 Murojaatlar** → **+ Yangi murojaat**
2. Bemorni tanlang (qidiruvni ham qo'llasangiz bo'ladi)
3. Shifokorni tanlang — uning narxi yonida ko'rsatiladi
4. Murojaat sanasini belgilang
5. Tashxisni kiriting (ixtiyoriy, keyin qo'shsa ham bo'ladi)

### Qadam 2: Protseduralar
- O'ng tomondagi ro'yxatdan kerakli protseduralarni belgilang
- Har biri uchun **soni**ni o'rnating (masalan, 5 ta inyeksiya)

### Qadam 3: Yakuniy hisob
- O'ng pastki kartochkada **avto-hisob** ko'rsatiladi:
  - Konsultatsiya
  - Protseduralar yig'indisi
  - **Jami summa** (chegirmasiz)
- Saqlashda chegirma server tomonida bemor toifasiga qarab qo'llaniladi.

### Qadam 4: Saqlash
**💾 Murojaatni saqlash** tugmasi → murojaat sahifasiga o'tasiz.

---

## 💰 5. To'lov

Murojaat sahifasida (`/visits/<id>`):
- **🔄 Qayta hisoblash** — agar protsedura/konsultatsiya o'zgartirilgan bo'lsa
- **💰 To'landi** — bemor pul to'laganidan keyin
- **✗ Bekor qilish** — agar bemor kelmasa

Holat ranglari:
- 🟡 **Kutilmoqda** — to'lov hali kelmagan
- 🟢 **To'langan** — yakuniy holat
- 🔴 **Bekor qilingan** — murojaat amalga oshmagan

---

## 📊 6. Dashboard (Bosh ekran)

Dashboard'da quyidagilar ko'rinadi:
- **Bugungi murojaatlar** soni va jami
- **Bugungi/oylik daromad**
- **Kutilayotgan to'lovlar**
- **30 kunlik daromad grafigi**
- **Mutaxassislik bo'yicha taqsimot** (pie chart)
- **Top shifokorlar** (bar chart)
- **Chegirmalar bo'yicha jadval**

### Excel'ga eksport
Yuqori o'ng burchakda **📥 Excel'ga yuklab olish** — oxirgi 30 kun daromad hisobotini Excel formatda yuklab oladi.

---

## 📑 7. Bemor tarixi PDF

Backend'dan to'g'ridan-to'g'ri PDF olish:
```
GET /api/reports/export/patient-history/<id>/
```

Bu chiqaradi:
- Bemor ma'lumotlari
- Barcha murojaatlar jadval ko'rinishida
- Tashxis, summa, holat

---

## 🛡 8. Foydalanuvchi rollari

| Rol | Imkoniyatlar |
|-----|--------------|
| **admin** | Hammasi: foydalanuvchilar, sozlamalar, hammasi |
| **registrator** | Bemorlar, murojaatlar, to'lovlar (qo'shish, tahrirlash) |
| **doctor** | Murojaatlarni ko'rish va tashxis kiritish |

> Rol biriktirish: `python manage.py setup_groups` ishga tushiring, so'ng admin paneldan foydalanuvchini guruhga qo'shing.

---

## 🆘 9. Tez-tez beriladigan savollar

### "Bemor allaqachon mavjud" deyilsa nima qilish?
Telefon raqami yagona bo'lishi kerak. Bemor allaqachon ro'yxatda — qidirib toping.

### Murojaat summasi noto'g'ri ko'rsatilmoqda
Murojaat detalida **🔄 Qayta hisoblash** ni bosing.

### Chegirma qo'llanmadi
- Bemor toifasi belgilanganligini tekshiring
- Toifa **Faolmi** ekanligini tekshiring (admin paneldan)
- Murojaatda **Qayta hisoblash** ni bosing

### Eski narx asosida hisoblanmoqda
Bu xato emas. **`price_at_time`** murojaat yaratilgan paytdagi narxni saqlaydi (tarix uchun). Keyin protsedura narxi o'zgarsa ham, eski murojaatlarga ta'sir qilmaydi.

---

## 📞 Texnik yordam

Muammoga duch kelsangiz:
1. Brauzer console'da xatoni tekshiring (F12)
2. Admin bilan bog'laning
3. GitHub Issues: https://github.com/Jamoliddin007/polyclinic-management/issues
