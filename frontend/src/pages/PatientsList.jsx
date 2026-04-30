import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import PageHeader from '../components/PageHeader.jsx';
import Table from '../components/Table.jsx';
import { listPatients, deletePatient } from '../api/patients.js';
import { genderLabel } from '../utils/format.js';

export default function PatientsList() {
  const [patients, setPatients] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchData = () => {
    setLoading(true);
    listPatients({ search })
      .then((data) => setPatients(data.results || data))
      .catch(() => toast.error('Maʼlumot yuklanmadi'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    const t = setTimeout(fetchData, 300);
    return () => clearTimeout(t);
  }, [search]);

  const handleDelete = async (id) => {
    if (!window.confirm('Ushbu bemorni o\'chirishni xohlaysizmi?')) return;
    try {
      await deletePatient(id);
      toast.success('O\'chirildi');
      fetchData();
    } catch {
      toast.error('Xatolik yuz berdi');
    }
  };

  const columns = [
    { key: 'id',          label: 'ID' },
    { key: 'full_name',   label: 'F.I.O.' },
    { key: 'phone',       label: 'Telefon' },
    { key: 'age',         label: 'Yoshi' },
    { key: 'gender',      label: 'Jinsi', render: (r) => genderLabel(r.gender) },
    { key: 'discount_category_name', label: 'Chegirma', render: (r) => r.discount_category_name || '—' },
    {
      key: 'actions',
      label: 'Amallar',
      render: (r) => (
        <div className="flex gap-2">
          <Link to={`/patients/${r.id}/edit`} className="text-primary-600 hover:underline">Tahrirlash</Link>
          <button onClick={(e) => { e.stopPropagation(); handleDelete(r.id); }} className="text-red-600 hover:underline">
            O'chirish
          </button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="Bemorlar"
        subtitle={`Jami: ${patients.length}`}
        actions={<Link to="/patients/new" className="btn-primary">+ Yangi bemor</Link>}
      />

      <div className="mb-4">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="🔍 Qidirish: ism, telefon, manzil..."
          className="input max-w-md"
        />
      </div>

      {loading ? <div className="card p-8 text-center">Yuklanmoqda...</div> : <Table columns={columns} data={patients} />}
    </div>
  );
}
