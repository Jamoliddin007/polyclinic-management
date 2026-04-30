import { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import PageHeader from '../components/PageHeader.jsx';
import { listPatients } from '../api/patients.js';
import { listDoctors } from '../api/doctors.js';
import { listProcedureTypes, createVisit } from '../api/visits.js';
import { formatMoney } from '../utils/format.js';

export default function VisitCreate() {
  const navigate = useNavigate();
  const [patients,   setPatients]   = useState([]);
  const [doctors,    setDoctors]    = useState([]);
  const [procedures, setProcedures] = useState([]);

  const [form, setForm] = useState({
    patient: '', primary_doctor: '',
    visit_date: new Date().toISOString().slice(0, 10),
    diagnosis: '',
  });
  const [selected, setSelected] = useState([]); // [{ procedure_type, quantity }]

  useEffect(() => {
    listPatients({ page_size: 200 }).then((d) => setPatients(d.results || d));
    listDoctors({ is_active: true, page_size: 200 }).then((d) => setDoctors(d.results || d));
    listProcedureTypes().then((d) => setProcedures((d.results || d).filter((p) => p.is_active)));
  }, []);

  const selectedDoctor = useMemo(
    () => doctors.find((d) => String(d.id) === String(form.primary_doctor)),
    [doctors, form.primary_doctor],
  );

  const subtotal = useMemo(() => {
    const procSum = selected.reduce((sum, item) => {
      const p = procedures.find((x) => x.id === item.procedure_type);
      return sum + (Number(p?.base_price || 0) * item.quantity);
    }, 0);
    const consultPrice = Number(selectedDoctor?.final_price || 0);
    return procSum + consultPrice;
  }, [selected, procedures, selectedDoctor]);

  const toggleProcedure = (id) => {
    setSelected((curr) => {
      const exists = curr.find((x) => x.procedure_type === id);
      if (exists) return curr.filter((x) => x.procedure_type !== id);
      return [...curr, { procedure_type: id, quantity: 1 }];
    });
  };

  const updateQty = (id, qty) => {
    setSelected((curr) => curr.map((x) => x.procedure_type === id ? { ...x, quantity: Math.max(1, qty) } : x));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.patient || !form.primary_doctor) {
      toast.error('Bemor va shifokorni tanlang');
      return;
    }
    try {
      const visit = await createVisit({ ...form, procedures: selected });
      toast.success(`Murojaat yaratildi #${visit.id}`);
      navigate(`/visits/${visit.id}`);
    } catch (err) {
      toast.error('Xatolik: ' + (err.response?.data?.detail || 'noma\'lum'));
    }
  };

  return (
    <div>
      <PageHeader title="Yangi murojaat" />

      <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="card p-6 space-y-4">
            <h3 className="font-semibold">1. Bemor va shifokor</h3>
            <div>
              <label className="block text-sm mb-1">Bemor</label>
              <select required value={form.patient} onChange={(e) => setForm({ ...form, patient: e.target.value })} className="input">
                <option value="">— tanlang —</option>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.full_name} — {p.phone}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm mb-1">Shifokor</label>
              <select required value={form.primary_doctor} onChange={(e) => setForm({ ...form, primary_doctor: e.target.value })} className="input">
                <option value="">— tanlang —</option>
                {doctors.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.full_name} — {d.specialty_name} ({formatMoney(d.final_price)})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm mb-1">Murojaat sanasi</label>
              <input type="date" value={form.visit_date} onChange={(e) => setForm({ ...form, visit_date: e.target.value })} className="input" />
            </div>
            <div>
              <label className="block text-sm mb-1">Tashxis</label>
              <textarea value={form.diagnosis} onChange={(e) => setForm({ ...form, diagnosis: e.target.value })} className="input" rows="3" />
            </div>
          </div>

          <div className="card p-6">
            <h3 className="font-semibold mb-3">2. Protseduralar</h3>
            <div className="space-y-2 max-h-96 overflow-auto">
              {procedures.map((p) => {
                const sel = selected.find((x) => x.procedure_type === p.id);
                return (
                  <div key={p.id} className="flex items-center justify-between p-2 hover:bg-slate-50 rounded">
                    <label className="flex items-center gap-2 flex-1 cursor-pointer">
                      <input type="checkbox" checked={!!sel} onChange={() => toggleProcedure(p.id)} />
                      <span>{p.name}</span>
                      <span className="text-slate-500 text-sm">— {formatMoney(p.base_price)}</span>
                    </label>
                    {sel && (
                      <input
                        type="number" min="1" value={sel.quantity}
                        onChange={(e) => updateQty(p.id, parseInt(e.target.value, 10))}
                        className="input w-20"
                      />
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <div className="card p-6 h-fit lg:sticky lg:top-6">
          <h3 className="font-semibold mb-3">Yakuniy hisob</h3>
          <div className="space-y-2 text-sm">
            <Row label="Konsultatsiya" value={formatMoney(selectedDoctor?.final_price || 0)} />
            <Row label="Protseduralar" value={`${selected.length} ta`} />
            <hr className="my-2" />
            <Row label="Jami (chegirmasiz)" value={formatMoney(subtotal)} bold />
            <p className="text-xs text-slate-500 mt-2">Chegirma server tomonida bemor toifasi asosida qo'llaniladi.</p>
          </div>
          <button type="submit" className="btn-primary w-full mt-6">💾 Murojaatni saqlash</button>
        </div>
      </form>
    </div>
  );
}

function Row({ label, value, bold }) {
  return (
    <div className={`flex justify-between ${bold ? 'font-semibold text-base' : ''}`}>
      <span>{label}</span>
      <span>{value}</span>
    </div>
  );
}
