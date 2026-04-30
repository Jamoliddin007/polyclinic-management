import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import PageHeader from '../components/PageHeader.jsx';
import { getVisit, markVisitPaid, cancelVisit, recalculateVisit } from '../api/visits.js';
import {
  formatMoney, formatDate, paymentStatusLabel, paymentStatusColor,
} from '../utils/format.js';

export default function VisitDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [visit, setVisit] = useState(null);

  const load = () => getVisit(id).then(setVisit).catch(() => toast.error('Yuklanmadi'));
  useEffect(() => { load(); }, [id]);

  const handleAction = async (fn, msg) => {
    try {
      await fn(id);
      toast.success(msg);
      load();
    } catch {
      toast.error('Xatolik');
    }
  };

  if (!visit) return <div className="card p-8 text-center">Yuklanmoqda...</div>;

  return (
    <div>
      <PageHeader
        title={`Murojaat #${visit.id}`}
        subtitle={`${visit.patient_name} — ${formatDate(visit.visit_date)}`}
        actions={
          <>
            <button onClick={() => handleAction(recalculateVisit, 'Qayta hisoblandi')} className="btn-secondary">🔄 Qayta hisoblash</button>
            {visit.payment_status === 'PENDING' && (
              <button onClick={() => handleAction(markVisitPaid, 'To\'landi')} className="btn-primary">💰 To'landi</button>
            )}
            {visit.payment_status !== 'CANCELLED' && (
              <button onClick={() => handleAction(cancelVisit, 'Bekor qilindi')} className="btn-danger">✗ Bekor qilish</button>
            )}
          </>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <Card title="Asosiy ma'lumotlar">
            <Row label="Bemor"     value={visit.patient_name} />
            <Row label="Shifokor"  value={visit.doctor_name} />
            <Row label="Sana"      value={formatDate(visit.visit_date)} />
            <Row label="Holat"     value={
              <span className={`px-2 py-1 rounded text-xs ${paymentStatusColor(visit.payment_status)}`}>
                {paymentStatusLabel(visit.payment_status)}
              </span>
            } />
          </Card>

          {visit.diagnosis && (
            <Card title="Tashxis">
              <p>{visit.diagnosis}</p>
            </Card>
          )}

          <Card title="Protseduralar">
            {visit.procedures?.length ? (
              <table className="w-full text-sm">
                <thead className="text-left text-slate-500 border-b">
                  <tr>
                    <th className="py-2">Nomi</th>
                    <th>Narx</th>
                    <th>Soni</th>
                    <th className="text-right">Summa</th>
                  </tr>
                </thead>
                <tbody>
                  {visit.procedures.map((p) => (
                    <tr key={p.id} className="border-b last:border-0">
                      <td className="py-2">{p.procedure_name}</td>
                      <td>{formatMoney(p.price_at_time)}</td>
                      <td>{p.quantity}</td>
                      <td className="text-right">{formatMoney(p.subtotal)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : <p className="text-slate-500">Protseduralar yo'q</p>}
          </Card>

          {visit.consultations?.length > 0 && (
            <Card title="Qo'shimcha konsultatsiyalar">
              {visit.consultations.map((c) => (
                <div key={c.id} className="flex justify-between py-1 border-b last:border-0">
                  <span>{c.doctor_name}</span>
                  <span>{formatMoney(c.price_at_time)}</span>
                </div>
              ))}
            </Card>
          )}
        </div>

        <div className="space-y-4">
          <Card title="Hisob-kitob">
            <Row label="Subtotal"  value={formatMoney(visit.subtotal)} />
            <Row label="Chegirma"  value={`-${formatMoney(visit.discount_amount)}`} />
            <hr className="my-2" />
            <Row label="Yakuniy" value={formatMoney(visit.total_cost)} bold />
          </Card>
        </div>
      </div>
    </div>
  );
}

function Card({ title, children }) {
  return (
    <div className="card p-6">
      <h3 className="font-semibold mb-3">{title}</h3>
      {children}
    </div>
  );
}

function Row({ label, value, bold }) {
  return (
    <div className={`flex justify-between py-1 ${bold ? 'font-bold text-lg' : ''}`}>
      <span className="text-slate-600">{label}</span>
      <span>{value}</span>
    </div>
  );
}
