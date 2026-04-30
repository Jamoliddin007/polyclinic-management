import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore.js';

const NAV = [
  { to: '/dashboard', label: '📊 Dashboard' },
  { to: '/patients',  label: '👥 Bemorlar' },
  { to: '/doctors',   label: '👨‍⚕️ Shifokorlar' },
  { to: '/visits',    label: '📅 Murojaatlar' },
];

export default function Layout() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex">
      <aside className="w-64 bg-slate-900 text-white p-6 flex flex-col">
        <h1 className="text-xl font-bold mb-8">🏥 Poliklinika</h1>

        <nav className="flex-1 space-y-1">
          {NAV.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`block px-3 py-2 rounded-md transition-colors ${
                pathname.startsWith(item.to)
                  ? 'bg-primary-600 text-white'
                  : 'text-slate-300 hover:bg-slate-800'
              }`}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="mt-auto pt-6 border-t border-slate-700">
          <p className="text-sm text-slate-400 mb-2">{user?.username || 'Foydalanuvchi'}</p>
          <button onClick={handleLogout} className="text-sm text-red-400 hover:text-red-300">
            🚪 Chiqish
          </button>
        </div>
      </aside>

      <main className="flex-1 p-8 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}
