import React, { useState, useEffect } from 'react';

export default function Navbar({
  isLoggedIn,
  currentUser,
  currentView,
  onOpenLogin,
  onLogout,
  onNavigate,
}) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState('home');

  useEffect(() => {
    if (currentView !== 'landing') return;

    const handleScroll = () => {
      const sections = ['home', 'how-it-works', 'features', 'docs', 'login'];
      const scrollPosition = window.scrollY + 120;

      for (const sectionId of sections) {
        const el = document.getElementById(sectionId);
        if (el) {
          const top = el.offsetTop;
          const height = el.offsetHeight;
          if (scrollPosition >= top && scrollPosition < top + height) {
            setActiveSection(sectionId);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [currentView]);

  const handleNavClick = (e, item) => {
    e.preventDefault();
    setMobileMenuOpen(false);

    if (item.id === 'dashboard') {
      if (isLoggedIn) {
        onNavigate('dashboard');
      } else {
        onOpenLogin();
      }
      return;
    }

    if (item.id === 'login') {
      if (isLoggedIn) {
        onNavigate('dashboard');
      } else {
        onOpenLogin();
      }
      return;
    }

    // Standard section link:
    onNavigate('landing', item.id);
  };

  const navItems = [
    { label: 'How it works', id: 'how-it-works' },
    { label: 'Features', id: 'features' },
    { label: 'Docs', id: 'docs' },
    { label: 'Dashboard', id: 'dashboard' },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#F5F5F5]/85 backdrop-blur-md transition-all duration-300 border-b border-[#DAD7D7]/50 shadow-sm">
      <div className="max-w-[1440px] mx-auto px-6 lg:px-16 h-[72px] lg:h-[88px] flex items-center justify-between">
        
        {/* Brand Logo with QUBIS name */}
        <button 
          onClick={() => onNavigate('landing', 'home')}
          className="font-orbitron font-extrabold text-xl lg:text-2xl text-gradient-orbitron tracking-tight hover:opacity-90 transition-opacity flex items-center gap-2 cursor-pointer"
          aria-label="QUBIS Home"
        >
          <span>QUBIS</span>
          {currentView === 'dashboard' && (
            <span className="hidden sm:inline-block px-2 py-0.5 rounded-full text-[10px] font-sans font-semibold bg-orange-100 text-[#D35C07] tracking-normal border border-orange-200">
              Live Console
            </span>
          )}
        </button>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8 lg:gap-12 xl:gap-16 font-inter text-[17px] lg:text-[19px] font-light text-black">
          {navItems.map((item) => {
            const isActive =
              (currentView === 'dashboard' && item.id === 'dashboard') ||
              (currentView === 'landing' && activeSection === item.id);

            return (
              <button
                key={item.label}
                onClick={(e) => handleNavClick(e, item)}
                className={`relative py-1 transition-colors duration-200 hover:text-tm-orange cursor-pointer bg-transparent border-none ${
                  isActive ? 'text-tm-orange font-normal' : 'text-black'
                }`}
              >
                <span className="flex items-center gap-1.5">
                  {item.label}
                  {item.id === 'dashboard' && (
                    <span className={`w-2 h-2 rounded-full ${isLoggedIn ? 'bg-[#16865D] animate-pulse' : 'bg-tm-orange/70'}`} />
                  )}
                </span>
                {isActive && (
                  <span className="absolute bottom-0 left-0 right-0 h-[2px] bg-tm-orange rounded-full animate-fade-in" />
                )}
              </button>
            );
          })}
        </nav>

        {/* Right CTA / Auth Status */}
        <div className="hidden md:flex items-center gap-3">
          {isLoggedIn ? (
            <div className="flex items-center gap-3">
              {currentView === 'landing' ? (
                <button
                  onClick={() => onNavigate('dashboard')}
                  className="px-4 py-2 rounded-full bg-gradient-to-r from-[#FEB048] to-[#D35C07] text-black font-medium text-sm shadow-sm hover:shadow hover:scale-[1.02] transition-all flex items-center gap-2 cursor-pointer"
                >
                  <span>Open Dashboard</span>
                  <span className="w-2 h-2 rounded-full bg-white animate-ping" />
                </button>
              ) : (
                <button
                  onClick={() => onNavigate('landing')}
                  className="px-3.5 py-1.5 rounded-full bg-white/80 border border-[#DAD7D7] text-black font-medium text-xs hover:bg-white hover:border-[#D35C07] transition-all flex items-center gap-1.5 shadow-sm cursor-pointer"
                >
                  <span>← Back to Landing</span>
                </button>
              )}

              {/* User Profile Pill */}
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/80 border border-[#DAD7D7] shadow-sm">
                <div className="w-6 h-6 rounded-full bg-gradient-to-br from-[#FEB048] to-[#D35C07] text-black font-bold text-[10px] flex items-center justify-center">
                  SA
                </div>
                <span className="text-xs font-semibold text-black/80">{currentUser?.name || 'Sayak Adak'}</span>
              </div>

              {/* Logout Button */}
              <button
                onClick={onLogout}
                title="Sign out"
                className="text-xs text-black/50 hover:text-[#D35C07] px-2 py-1 rounded transition-colors cursor-pointer"
              >
                Log Out
              </button>
            </div>
          ) : (
            <button
              onClick={onOpenLogin}
              className="px-6 py-2 rounded-full bg-white/90 border border-[#DAD7D7] hover:border-[#D35C07] hover:text-[#D35C07] text-black font-medium text-sm shadow-sm hover:shadow transition-all flex items-center gap-2 cursor-pointer"
            >
              <svg className="w-4 h-4 text-[#D35C07]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
              <span>Login</span>
            </button>
          )}
        </div>

        {/* Mobile Hamburger Button */}
        <button
          type="button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 text-black hover:text-tm-orange focus:outline-none"
          aria-label="Toggle navigation menu"
        >
          <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {mobileMenuOpen ? (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
            )}
          </svg>
        </button>
      </div>

      {/* Mobile Dropdown Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#F5F5F5]/98 border-b border-[#DAD7D7] px-6 py-6 shadow-xl animate-in slide-in-from-top">
          <nav className="flex flex-col gap-3 font-inter text-base font-light text-black">
            {navItems.map((item) => (
              <button
                key={item.label}
                onClick={(e) => handleNavClick(e, item)}
                className="py-2.5 px-3 rounded-lg text-left transition-colors hover:bg-orange-50 hover:text-tm-orange flex items-center justify-between"
              >
                <span>{item.label}</span>
                {item.id === 'dashboard' && (
                  <span className={`w-2 h-2 rounded-full ${isLoggedIn ? 'bg-[#16865D]' : 'bg-tm-orange'}`} />
                )}
              </button>
            ))}

            <div className="pt-4 border-t border-[#DAD7D7] flex flex-col gap-2">
              {isLoggedIn ? (
                <>
                  <div className="flex items-center justify-between py-2 px-3 bg-white rounded-lg border border-[#DAD7D7]">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-tm-orange text-white text-xs flex items-center justify-center font-bold">
                        SA
                      </div>
                      <span className="text-xs font-semibold">{currentUser?.name || 'Sayak Adak'}</span>
                    </div>
                    <span className="text-[10px] text-[#16865D] font-bold">Logged In</span>
                  </div>
                  <button
                    onClick={() => {
                      setMobileMenuOpen(false);
                      onNavigate(currentView === 'dashboard' ? 'landing' : 'dashboard');
                    }}
                    className="w-full py-2.5 rounded-lg bg-gradient-to-r from-[#FEB048] to-[#D35C07] text-black font-semibold text-sm"
                  >
                    {currentView === 'dashboard' ? 'Back to Landing Page' : 'Open Dashboard'}
                  </button>
                  <button
                    onClick={() => {
                      setMobileMenuOpen(false);
                      onLogout();
                    }}
                    className="w-full py-2 text-xs text-red-600 font-medium"
                  >
                    Sign Out
                  </button>
                </>
              ) : (
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    onOpenLogin();
                  }}
                  className="w-full py-2.5 rounded-lg bg-gradient-to-r from-[#FEB048] to-[#D35C07] text-black font-semibold text-sm"
                >
                  Login to QUBIS
                </button>
              )}
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}
