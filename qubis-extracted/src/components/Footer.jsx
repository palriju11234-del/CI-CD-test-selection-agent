import React from 'react';

export default function Footer() {
  return (
    <footer className="w-full h-[100px] bg-tm-dark text-[#EEEEEE] flex items-center justify-between px-6 lg:px-20 text-[13px] border-t border-white/10">
      <div className="flex items-center gap-3">
        <span className="font-orbitron font-extrabold text-[16px] text-tm-amber tracking-wider">
          QUBIS
        </span>
        <span className="text-white/40 hidden sm:inline">|</span>
        <span className="text-white/60 font-inter hidden sm:inline">
          Intelligent Test Acceleration
        </span>
      </div>
      <span className="font-inter text-white/70 text-[12px] sm:text-[13px]">
        AI-powered CI/CD test selection
      </span>
    </footer>
  );
}
