export const formatMoney = (value) => {
  if (value == null) return '—';
  return new Intl.NumberFormat('uz-UZ').format(value) + " so'm";
};

export const formatDate = (value) => {
  if (!value) return '—';
  return new Date(value).toLocaleDateString('uz-UZ');
};

export const formatDateTime = (value) => {
  if (!value) return '—';
  return new Date(value).toLocaleString('uz-UZ');
};

export const paymentStatusLabel = (status) =>
  ({ PENDING: 'Kutilmoqda', PAID: "To'langan", CANCELLED: 'Bekor qilingan' }[status] || status);

export const paymentStatusColor = (status) =>
  ({
    PENDING:   'bg-yellow-100 text-yellow-800',
    PAID:      'bg-green-100 text-green-800',
    CANCELLED: 'bg-red-100 text-red-800',
  }[status] || 'bg-slate-100 text-slate-800');

export const genderLabel = (g) => ({ M: 'Erkak', F: 'Ayol' }[g] || g);
