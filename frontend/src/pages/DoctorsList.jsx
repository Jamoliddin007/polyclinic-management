import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import PageHeader from '../components/PageHeader.jsx';
import Table from '../components/Table.jsx';
import { listDoctors, listSpecialties } from '../api/doctors.js';
import { formatMoney } from '../utils/format.js';

export default function DoctorsList() {
  const [doctors, setDoctors] = useState([]);
  const [specialties, setSpecialties] = useState([]);
  const [filter, setFilter] = useState({ specialty: '', search: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listSpecialties().then((d) => setSpecialties(d.results || d));
  }, []);

  useEffect(() => {
    setLoading(true);
    listDoctors({ specialty: filter.specialty || undefined, search: filter.search })
      .then((data) => setDoctors(data.results || data))
      .catch(() => toast.error('Yuklanmadi'))
      .finally(() => setLoading(false));
  }, [filter.specialty, filter.search]);

  const columns = [
    { key: 'id',                  label: 'ID' },
    { key: 'full_name',           label: 'F.I.O.' },
    { key: 'specialty_name',      label: 'Mutaxassislik' },
    { key: 'qualification_name',  label: 'Malaka' },
    { key: 'consultation_price',  label: 'Asosiy narx', render: (r) => formatMoney(r.consultation_price) },
    { key: 'final_price',         label: 'Yakuniy narx', render: (r) => formatMoney(r.final_price) },
    {
      key: 'is_active',
      label: 'Holati',
      render: (r) => (
        <span className={`px-2 py-1 rounded text-xs ${r.is_active ? 'bg-green-100 text-green-800' : 'bg-slate-100 text-slate-600'}`}>
          {r.is_active ? 'Faol' : 'Nofaol'}
        </span>
      ),
    },
  ];

  return (
    <div>
      <PageHeader title="Shifokorlar" subtitle={`Jami: ${doctors.length}`} />

      <div className="flex gap-3 mb-4">
        <input
          value={filter.search}
          onChange={(e) => setFilter({ ...filter, search: e.target.value })}
          placeholder="🔍 Ism..."
          className="input max-w-xs"
        />
        <select
          value={filter.specialty}
          onChange={(e) => setFilter({ ...filter, specialty: e.target.value })}
          className="input max-w-xs"
        >
          <option value="">— Hamma mutaxassisliklar —</option>
          {specialties.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>
      </div>

      {loading ? <div className="card p-8 text-center">Yuklanmoqda...</div> : <Table columns={columns} data={doctors} />}
    </div>
  );
}
