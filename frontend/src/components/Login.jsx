import React from 'react';

export default function Login({ isLoggedIn, onOpenLogin, onViewDemo }) {
  return (
    <section 
      id="login" 
      className="relative w-full py-24 lg:py-32 bg-[#F5F5F5] flex items-center justify-center px-6"
    >
      <div className="max-w-[700px] w-full text-center px-8 py-14 sm:px-16 sm:py-16 rounded-[28px] card-new-glass border border-[#DAD7D7]">
        <p className="text-tm-orange font-semibold text-[13px] tracking-[0.16em] uppercase mb-3">
          QUBIS AI TEST ENGINE
        </p>
        <h2 className="font-inter text-[34px] sm:text-[44px] text-black font-normal leading-tight mb-4">
          Ready to make CI faster?
        </h2>
        <p className="font-inter font-light text-[16px] sm:text-[18px] text-black/70 leading-relaxed mb-8 max-w-[500px] mx-auto">
          Start accelerating your continuous integration with intelligent test selection. Sign in or explore the live dashboard in demo mode right now.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button
            type="button"
            onClick={onOpenLogin}
            className="btn-get-started inline-flex items-center justify-center px-10 h-[64px] rounded-[50px] font-inter font-medium text-[20px] text-black tracking-normal cursor-pointer hover:scale-[1.02] transition-transform"
          >
            {isLoggedIn ? 'Access Dashboard' : 'Sign In / Register'}
          </button>

          <button
            type="button"
            onClick={onViewDemo}
            className="btn-view-demo inline-flex items-center justify-center px-8 h-[64px] rounded-[50px] font-inter font-medium text-[18px] text-black tracking-normal cursor-pointer hover:scale-[1.02] transition-transform"
          >
            ⚡ Instant Demo Access
          </button>
        </div>
      </div>
    </section>
  );
}
