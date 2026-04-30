import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import PageHeader from '../components/PageHeader.jsx';
import {
  getPatient, createPatient, updatePatient, listDiscountCategories,
} from '../api/patients.js';

export default function PatientForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = !!id;

  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm();
  const [discounts, setDiscounts] = useState([]);

  useEffect(() => {
    listDiscountCategories().then((d) => setDiscounts(d.results || d));
    if (isEdit) {
      getPatient(id).then((p) => reset({
        ...p,
        discount_category: p.discount_category || '',
      }));
    }
  }, [id]);

  const onSubmit = async (data) => {
    const payload = {
      ...data,
      discount_category: data.discount_category || null,
    };
    try {
      if (isEdit) {
        await updatePatient(id, payload);
        toast.success('Bemor yangilandi');
      } else {
        await createPatient(payload);
        toast.success('Bemor qo\'shildi');
      }
      navigate('/patients');
    } catch (err) {
      toast.error('Xatolik: ' + (err.response?.data?.phone?.[0] || 'noma\'lum'));
    }
  };

  return (
    <div>
      <PageHeader title={isEdit ? 'Bemorni tahrirlash' : 'Yangi bemor'} />

      <form onSubmit={handleSubmit(onSubmit)} className="card p-6 max-w-2xl space-y-4">
        <Field label="F.I.O." error={errors.full_name?.message}>
          <input {...register('full_name', { required: 'Majburiy' })} className="input" />
        </Field>

        <div className="grid grid-cols-2 gap-4">
          <Field label="Tug'ilgan sana" error={errors.birth_date?.message}>
            <input type="date" {...register('birth_date', { required: 'Majburiy' })} className="input" />
          </Field>
          <Field label="Jinsi" error={errors.gender?.message}>
            <select {...register('gender', { required: 'Majburiy' })} className="input">
              <option value="">— tanlang —</option>
              <option value="M">Erkak</option>
              <option value="F">Ayol</option>
            </select>
          </Field>
        </div>

        <Field label="Telefon" error={errors.phone?.message}>
          <input {...register('phone', { required: 'Majburiy' })} className="input" placeholder="+998901234567" />
        </Field>

        <Field label="Manzil">
          <input {...register('address')} className="input" />
        </Field>

        <Field label="Chegirma toifasi">
          <select {...register('discount_category')} className="input">
            <option value="">— yo'q —</option>
            {discounts.map((d) => (
              <option key={d.id} value={d.id}>{d.name} ({d.percent}%)</option>
            ))}
          </select>
        </Field>

        <div className="flex gap-2 pt-4">
          <button type="submit" disabled={isSubmitting} className="btn-primary">
            {isSubmitting ? 'Saqlanmoqda...' : 'Saqlash'}
          </button>
          <button type="button" onClick={() => navigate('/patients')} className="btn-secondary">
            Bekor qilish
          </button>
        </div>
      </form>
    </div>
  );
}

function Field({ label, error, children }) {
  return (
    <div>
      <label className="block text-sm font-medium text-slate-700 mb-1">{label}</label>
      {children}
      {error && <p className="text-sm text-red-600 mt-1">{error}</p>}
    </div>
  );
}
