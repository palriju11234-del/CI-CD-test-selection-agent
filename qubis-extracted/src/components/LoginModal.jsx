import React, { useState } from 'react';

export default function LoginModal({ isOpen, onClose, onLoginSuccess }) {
  const [email, setEmail] = useState('sayak.adak@reviewer.internal');
  const [password, setPassword] = useState('••••••••••••');
  const [isLoading, setIsLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      onLoginSuccess({
        name: 'Sayak Adak',
        role: 'Judge / Reviewer',
        email: email || 'sayak.adak@reviewer.internal',
      });
    }, 450);
  };

  const handleQuickDemo = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      onLoginSuccess({
        name: 'Sayak Adak',
        role: 'Judge / Reviewer',
        email: 'sayak.adak@reviewer.internal',
      });
    }, 300);
  };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in"
      onClick={onClose}
    >
      <div 
        className="relative w-full max-w-md p-8 rounded-[24px] bg-white/95 backdrop-blur-xl border border-[#DAD7D7] shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Decorative corner glows matching landing page */}
        <div 
          className="absolute -top-10 -right-10 w-36 h-36 rounded-full pointer-events-none opacity-40 blur-2xl"
          style={{ background: 'radial-gradient(circle, #FEB048 0%, rgba(211,92,7,0) 70%)' }}
        />
        <div 
          className="absolute -bottom-10 -left-10 w-36 h-36 rounded-full pointer-events-none opacity-30 blur-2xl"
          style={{ background: 'radial-gradient(circle, #D35C07 0%, rgba(211,92,7,0) 70%)' }}
        />

        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-100 text-slate-500 hover:text-black hover:bg-slate-200 flex items-center justify-center transition-colors cursor-pointer"
          aria-label="Close login dialog"
        >
          ✕
        </button>

        {/* Logo & Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br from-[#FEB048] to-[#D35C07] text-white shadow-md mb-2">
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
            </svg>
          </div>
          <h3 className="font-orbitron font-extrabold text-2xl text-gradient-orbitron tracking-tight">
            QUBIS
          </h3>
          <p className="font-inter text-xs text-black/60 uppercase tracking-widest mt-0.5">
            AI Test Intelligence Login
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4 font-inter text-left">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Email Address
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="sayak.adak@reviewer.internal"
              className="w-full px-3.5 py-2.5 rounded-xl border border-[#DAD7D7] bg-white text-sm text-slate-900 focus:outline-none focus:border-tm-orange focus:ring-1 focus:ring-tm-orange transition-all"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl border border-[#DAD7D7] bg-white text-sm text-slate-900 focus:outline-none focus:border-tm-orange focus:ring-1 focus:ring-tm-orange transition-all"
            />
          </div>

          <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
            <label className="flex items-center gap-1.5 cursor-pointer">
              <input type="checkbox" defaultChecked className="rounded border-slate-300 text-tm-orange focus:ring-tm-orange" />
              <span>Remember me</span>
            </label>
            <button 
              type="button" 
              onClick={() => alert('Demo password reset link simulated for Sayak Adak.')}
              className="hover:text-tm-orange transition-colors text-slate-500 underline"
            >
              Forgot password?
            </button>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="btn-get-started w-full h-[52px] rounded-[50px] flex items-center justify-center font-inter font-medium text-base text-black mt-3 disabled:opacity-75 cursor-pointer hover:scale-[1.01] transition-transform"
          >
            {isLoading ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin" />
                Signing in...
              </span>
            ) : (
              'Sign In to Dashboard'
            )}
          </button>
        </form>

        {/* Divider */}
        <div className="relative my-5">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-[#DAD7D7]" />
          </div>
          <div className="relative flex justify-center text-[11px] uppercase text-slate-400">
            <span className="bg-white px-2">or 1-click reviewer access</span>
          </div>
        </div>

        {/* Quick Demo Button */}
        <button
          type="button"
          onClick={handleQuickDemo}
          disabled={isLoading}
          className="w-full py-3 px-4 rounded-xl border border-tm-orange/40 bg-orange-50/80 hover:bg-orange-100 text-tm-orange font-inter font-semibold text-xs transition-colors flex items-center justify-center gap-2 shadow-sm cursor-pointer"
        >
          <span>⚡ Enter as Demo Reviewer (Sayak Adak)</span>
        </button>
      </div>
    </div>
  );
}
