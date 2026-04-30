import { useEffect, useState } from 'react';
import PageHeader from '../components/PageHeader.jsx';
import { listPatients } from '../api/patients.js';
import { listDoctors } from '../api/doctors.js';
import { listVisits } from '../api/visits.js';
import { formatMoney } from '../utils/format.js';

function StatCard({ label, value, icon, color = 'primary' }) {
  return (
    <div className="card p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">{label}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
        <div className={`text-3xl text-${color}-500`}>{icon}</div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState({ patients: '...', doctors: '...', visits: '...', revenue: '...' });

  useEffect(() => {
    Promise.all([
      listPatients({ page_size: 1 }),
      listDoctors({ page_size: 1 }),
      listVisits({ page_size: 100 }),
    ]).then(([pat, doc, vis]) => {
      const visits = vis.results || vis;
      const paid = (visits || []).filter((v) => v.payment_status === 'PAID');
      const revenue = paid.reduce((sum, v) => sum + Number(v.total_cost || 0), 0);
      setStats({
        patients: pat.count ?? (pat.results?.length || 0),
        doctors:  doc.count ?? (doc.results?.length || 0),
        visits:   vis.count ?? visits.length,
        revenue,
      });
    }).catch((err) => {
      console.error('Dashboard load failed:', err);
    });
  }, []);

  return (
    <div>
      <PageHeader title="Dashboard" subtitle="Tizim holatining umumiy ko'rinishi" />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard label="Bemorlar"  value={stats.patients} icon="👥" />
        <StatCard label="Shifokorlar" value={stats.doctors} icon="👨‍⚕️" />
        <StatCard label="Murojaatlar" value={stats.visits} icon="📅" />
        <StatCard
          label="Daromad"
          value={typeof stats.revenue === 'number' ? formatMoney(stats.revenue) : '...'}
          icon="💰"
        />
      </div>

      <div className="card p-6 mt-6">
        <h3 className="font-semibold mb-2">📈 Diagrammalar va batafsil hisobotlar</h3>
        <p className="text-slate-500">
          Bosqich 6'da to'liq dashboard (oylik daromad, top shifokorlar, mutaxassislik diagrammasi) qo'shiladi.
        </p>
      </div>
    </div>
  );
}
