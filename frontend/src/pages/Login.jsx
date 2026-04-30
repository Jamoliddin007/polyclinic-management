import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { login } from '../api/auth.js';
import { useAuthStore } from '../store/authStore.js';

export default function Login() {
  const navigate = useNavigate();
  const setAuth = useAuthStore((s) => s.login);
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [loading, setLoading] = useState(false);

  const onSubmit = async (form) => {
    setLoading(true);
    try {
      const data = await login(form.username, form.password);
      setAuth(data.access, data.refresh, { username: form.username });
      toast.success('Xush kelibsiz!');
      navigate('/dashboard');
    } catch (err) {
      toast.error('Login yoki parol notoʻgʻri');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-primary-900 p-4">
      <div className="card w-full max-w-md p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-slate-900">🏥 Poliklinika</h1>
          <p className="text-slate-500 mt-2">Boshqaruv tizimiga kirish</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Login</label>
            <input
              {...register('username', { required: 'Login kiriting' })}
              className="input"
              placeholder="admin"
              autoFocus
            />
            {errors.username && <p className="text-sm text-red-600 mt-1">{errors.username.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Parol</label>
            <input
              {...register('password', { required: 'Parol kiriting' })}
              type="password"
              className="input"
              placeholder="••••••••"
            />
            {errors.password && <p className="text-sm text-red-600 mt-1">{errors.password.message}</p>}
          </div>

          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? 'Kirilmoqda...' : 'Kirish'}
          </button>
        </form>
      </div>
    </div>
  );
}
