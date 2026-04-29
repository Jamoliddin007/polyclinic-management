# 🏥 Polyclinic Management System — Class Diagram (UML)

Bu Class Diagram **Django models** bilan to'g'ridan-to'g'ri bog'lanadi. Har bir sinf — bu Django `Model`.

```mermaid
classDiagram
    direction LR

    class DiscountCategory {
        +int id
        +str name
        +Decimal percent
        +str description
        +bool is_active
        +calculate_discount(amount) Decimal
    }

    class Patient {
        +int id
        +str full_name
        +date birth_date
        +str gender
        +str phone
        +str address
        +DiscountCategory discount_category
        +datetime created_at
        +get_age() int
        +get_visit_history() QuerySet
    }

    class Specialty {
        +int id
        +str name
        +str description
        +get_doctors() QuerySet
    }

    class Qualification {
        +int id
        +str name
        +Decimal price_multiplier
    }

    class Doctor {
        +int id
        +str full_name
        +Specialty specialty
        +Qualification qualification
        +Decimal consultation_price
        +str phone
        +bool is_active
        +get_final_price() Decimal
        +get_today_visits() QuerySet
    }

    class ProcedureType {
        +int id
        +str name
        +Decimal base_price
        +int duration_minutes
        +str description
        +bool is_active
    }

    class Visit {
        +int id
        +Patient patient
        +Doctor primary_doctor
        +date visit_date
        +str diagnosis
        +Decimal subtotal
        +Decimal discount_amount
        +Decimal total_cost
        +str payment_status
        +calculate_total_cost() Decimal
        +apply_discount() Decimal
        +mark_as_paid() void
        +cancel() void
    }

    class VisitProcedure {
        +int id
        +Visit visit
        +ProcedureType procedure_type
        +Decimal price_at_time
        +int quantity
        +str notes
        +get_subtotal() Decimal
    }

    class VisitConsultation {
        +int id
        +Visit visit
        +Doctor doctor
        +Decimal price_at_time
        +str notes
    }

    class Payment {
        +int id
        +Visit visit
        +Decimal amount
        +str method
        +datetime paid_at
        +str receipt_number
        +generate_receipt() PDF
    }

    DiscountCategory "1" --o "*" Patient : has
    Specialty "1" --o "*" Doctor : employs
    Qualification "1" --o "*" Doctor : grants
    Patient "1" --* "*" Visit : creates
    Doctor "1" --o "*" Visit : conducts
    Visit "1" --* "*" VisitProcedure : contains
    ProcedureType "1" --o "*" VisitProcedure : type_of
    Visit "1" --* "*" VisitConsultation : contains
    Doctor "1" --o "*" VisitConsultation : provides
    Visit "1" --o "1" Payment : settled_by
```

---

## 🎯 Use Case Diagram (qo'shimcha — kim nima qiladi)

```mermaid
flowchart LR
    subgraph Actors[" "]
        Admin((👤 Admin))
        Reg((👤 Registrator))
        Doctor((👤 Shifokor))
        Patient((👤 Bemor))
    end

    subgraph System["🏥 Polyclinic Management System"]
        UC1[Bemorlarni boshqarish]
        UC2[Shifokorlarni boshqarish]
        UC3[Murojaat ro'yxatga olish]
        UC4[Protsedura biriktirish]
        UC5[Chegirma qo'llash]
        UC6[To'lov qabul qilish]
        UC7[Tashxis kiritish]
        UC8[Hisobot olish]
        UC9[Foydalanuvchilarni boshqarish]
        UC10[O'z murojaatlari tarixini ko'rish]
    end

    Admin --> UC1
    Admin --> UC2
    Admin --> UC8
    Admin --> UC9

    Reg --> UC1
    Reg --> UC3
    Reg --> UC4
    Reg --> UC5
    Reg --> UC6

    Doctor --> UC7
    Doctor --> UC4

    Patient --> UC10
```

---

## 🧠 Asosiy biznes-metodlar (Django'da implementatsiya)

### `Visit.calculate_total_cost()`

```python
def calculate_total_cost(self):
    """Konsultatsiyalar + protseduralar yig'indisi"""
    procedures_sum = self.visitprocedure_set.aggregate(
        total=Sum(F('price_at_time') * F('quantity'))
    )['total'] or 0

    consultations_sum = self.visitconsultation_set.aggregate(
        total=Sum('price_at_time')
    )['total'] or 0

    self.subtotal = procedures_sum + consultations_sum
    return self.subtotal
```

### `Visit.apply_discount()`

```python
def apply_discount(self):
    """Bemor toifasi bo'yicha chegirma qo'llash"""
    if self.patient.discount_category and self.patient.discount_category.is_active:
        percent = self.patient.discount_category.percent
        self.discount_amount = self.subtotal * (percent / 100)
    else:
        self.discount_amount = 0

    self.total_cost = self.subtotal - self.discount_amount
    return self.total_cost
```

### Signal: protsedura qo'shilganda avto-yangilash

```python
@receiver([post_save, post_delete], sender=VisitProcedure)
def update_visit_total(sender, instance, **kwargs):
    visit = instance.visit
    visit.calculate_total_cost()
    visit.apply_discount()
    visit.save()
```
