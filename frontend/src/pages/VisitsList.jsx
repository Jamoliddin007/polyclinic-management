import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import PageHeader from '../components/PageHeader.jsx';
import Table from '../components/Table.jsx';
import { listVisits } from '../api/visits.js';
import {
  formatMoney, formatDate, paymentStatusLabel, paymentStatusColor,
} from '../utils/format.js';

export default function VisitsList() {
  const navigate = useNavigate();
  const [visits, setVisits] = useState([]);
  const [statusFilter, setStatusFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    listVisits({ payment_status: statusFilter || undefined })
      .then((data) => setVisits(data.results || data))
      .catch(() => toast.error('Yuklanmadi'))
      .finally(() => setLoading(false));
  }, [statusFilter]);

  const columns = [
    { key: 'id',           label: '#' },
    { key: 'patient_name', label: 'Bemor' },
    { key: 'doctor_name',  label: 'Shifokor' },
    { key: 'specialty_name', label: 'Mutaxassislik' },
    { key: 'visit_date',   label: 'Sana', render: (r) => formatDate(r.visit_date) },
    { key: 'total_cost',   label: 'Summa', render: (r) => formatMoney(r.total_cost) },
    {
      key: 'payment_status',
      label: 'Holati',
      render: (r) => (
        <span className={`px-2 py-1 rounded text-xs ${paymentStatusColor(r.payment_status)}`}>
          {paymentStatusLabel(r.payment_status)}
        </span>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="Murojaatlar"
        subtitle={`Jami: ${visits.length}`}
        actions={<Link to="/visits/new" className="btn-primary">+ Yangi murojaat</Link>}
      />

      <div className="mb-4">
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className="input max-w-xs">
          <option value="">— Hamma holatlar —</option>
          <option value="PENDING">Kutilmoqda</option>
          <option value="PAID">To'langan</option>
          <option value="CANCELLED">Bekor qilingan</option>
        </select>
      </div>

      {loading ? (
        <div className="card p-8 text-center">Yuklanmoqda...</div>
      ) : (
        <Table columns={columns} data={visits} onRowClick={(r) => navigate(`/visits/${r.id}`)} />
      )}
    </div>
  );
}
