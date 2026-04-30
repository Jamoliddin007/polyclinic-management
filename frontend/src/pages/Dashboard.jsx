import { useEffect, useState } from 'react';
import {
  ResponsiveContainer,
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid,
  PieChart, Pie, Cell, Legend,
  BarChart, Bar,
} from 'recharts';
import PageHeader from '../components/PageHeader.jsx';
import {
  getDashboardKPI,
  getRevenue,
  getTopDoctors,
  getSpecialtyDistribution,
  getDiscountDistribution,
} from '../api/reports.js';
import { formatMoney } from '../utils/format.js';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#f97316'];

function StatCard({ label, value, icon, hint }) {
  return (
    <div className="card p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">{label}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
          {hint && <p className="text-xs text-slate-400 mt-1">{hint}</p>}
        </div>
        <div className="text-3xl">{icon}</div>
      </div>
    </div>
  );
}

function ChartCard({ title, action, children }) {
  return (
    <div className="card p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-semibold">{title}</h3>
        {action}
      </div>
      {children}
    </div>
  );
}

export default function Dashboard() {
  const [kpi, setKpi] = useState(null);
  const [revenue, setRevenue] = useState([]);
  const [topDoctors, setTopDoctors] = useState([]);
  const [specialty, setSpecialty] = useState([]);
  const [discount, setDiscount] = useState([]);

  useEffect(() => {
    getDashboardKPI().then(setKpi).catch(console.error);
    getRevenue().then((d) => setRevenue(d.data || [])).catch(console.error);
    getTopDoctors().then(setTopDoctors).catch(console.error);
    getSpecialtyDistribution().then(setSpecialty).catch(console.error);
    getDiscountDistribution().then(setDiscount).catch(console.error);
  }, []);

  const downloadExcel = () => {
    window.open(`${import.meta.env.VITE_API_URL || '/api'}/reports/export/revenue-excel/?days=30`, '_blank');
  };

  return (
    <div>
      <PageHeader
        title="Dashboard"
        subtitle="Analitik ko'rsatkichlar"
        actions={<button onClick={downloadExcel} className="btn-secondary">📥 Excel'ga yuklab olish</button>}
      />

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard label="Bugungi murojaatlar" value={kpi?.visits_today ?? '...'} icon="📅" hint={`Jami: ${kpi?.visits_total ?? '...'}`} />
        <StatCard label="Bugungi daromad"     value={kpi ? formatMoney(kpi.revenue_today) : '...'} icon="💰" />
        <StatCard label="Oylik daromad"       value={kpi ? formatMoney(kpi.revenue_month) : '...'} icon="📈" />
        <StatCard label="Kutilayotgan to'lov" value={kpi?.visits_pending ?? '...'} icon="⏳" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <ChartCard title="📈 Oxirgi 30 kun daromadi">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={revenue}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="visit_date" tickFormatter={(v) => v?.slice(5)} />
              <YAxis tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`} />
              <Tooltip formatter={(v) => formatMoney(v)} />
              <Line type="monotone" dataKey="net" stroke="#3b82f6" strokeWidth={2} name="Netto" />
              <Line type="monotone" dataKey="gross" stroke="#10b981" strokeWidth={2} name="Brutto" strokeDasharray="5 5" />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="🏥 Mutaxassislik bo'yicha murojaatlar">
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={specialty.filter((s) => s.visit_count > 0)}
                dataKey="visit_count"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label={(e) => e.name}
              >
                {specialty.map((_, idx) => (
                  <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="🥇 Top shifokorlar">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topDoctors} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="full_name" type="category" width={120} fontSize={11} />
              <Tooltip />
              <Bar dataKey="total_visits" fill="#3b82f6" name="Murojaatlar" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="💸 Chegirma toifalari">
          <table className="w-full text-sm">
            <thead className="text-left text-slate-500 border-b">
              <tr>
                <th className="py-2">Toifa</th>
                <th>%</th>
                <th>Bemorlar</th>
                <th className="text-right">Berilgan chegirma</th>
              </tr>
            </thead>
            <tbody>
              {discount.map((d) => (
                <tr key={d.id} className="border-b last:border-0">
                  <td className="py-2">{d.name}</td>
                  <td>{d.percent}%</td>
                  <td>{d.patients_count}</td>
                  <td className="text-right">{formatMoney(d.discount_given || 0)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </ChartCard>
      </div>
    </div>
  );
}
