import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar.jsx';
import Home from './pages/Home.jsx';
import Dashboard from './components/Dashboard.jsx';
import Footer from './components/Footer.jsx';
import LoginModal from './components/LoginModal.jsx';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return sessionStorage.getItem('qubis_auth') === 'true';
  });

  const [currentUser, setCurrentUser] = useState(() => {
    const saved = sessionStorage.getItem('qubis_user');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        // fallback
      }
    }
    return {
      name: 'Sayak Adak',
      role: 'Judge / Reviewer',
      email: 'sayak.adak@reviewer.internal',
    };
  });

  // 'landing' or 'dashboard'
  const [currentView, setCurrentView] = useState(() => {
    return sessionStorage.getItem('qubis_view') || 'landing';
  });

  const [showLoginModal, setShowLoginModal] = useState(false);
  const [toastMessage, setToastMessage] = useState(null);

  // Show temporary toast notification
  const showToast = (msg, duration = 3000) => {
    setToastMessage(msg);
    setTimeout(() => {
      setToastMessage(null);
    }, duration);
  };

  const handleLoginSuccess = (userData) => {
    const user = userData || {
      name: 'Sayak Adak',
      role: 'Judge / Reviewer',
      email: 'sayak.adak@reviewer.internal',
    };
    setIsLoggedIn(true);
    setCurrentUser(user);
    sessionStorage.setItem('qubis_auth', 'true');
    sessionStorage.setItem('qubis_user', JSON.stringify(user));
    setShowLoginModal(false);
    setCurrentView('dashboard');
    sessionStorage.setItem('qubis_view', 'dashboard');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    showToast(`Welcome, ${user.name}! Dashboard loaded successfully.`);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    sessionStorage.removeItem('qubis_auth');
    sessionStorage.removeItem('qubis_view');
    setCurrentView('landing');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    showToast('Signed out of QUBIS session.');
  };

  const handleOpenLogin = () => {
    setShowLoginModal(true);
  };

  const handleCloseLogin = () => {
    setShowLoginModal(false);
  };

  const handleDirectDemo = () => {
    handleLoginSuccess({
      name: 'Sayak Adak',
      role: 'Judge / Reviewer',
      email: 'sayak.adak@reviewer.internal',
    });
  };

  const handleNavigateToView = (view, sectionId = null) => {
    setCurrentView(view);
    sessionStorage.setItem('qubis_view', view);
    if (view === 'landing' && sectionId) {
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) {
          el.scrollIntoView({ behavior: 'smooth' });
        }
      }, 50);
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#F5F5F5] text-[#111111] selection:bg-orange-200 selection:text-orange-900 font-inter">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-[9999] px-5 py-3 rounded-xl bg-slate-900/95 text-white text-sm font-medium shadow-2xl border border-white/10 flex items-center gap-3 animate-fade-in backdrop-blur-md">
          <span className="w-2.5 h-2.5 rounded-full bg-[#39D39F] animate-pulse" />
          <span>{toastMessage}</span>
          <button
            onClick={() => setToastMessage(null)}
            className="text-white/60 hover:text-white text-xs ml-2"
          >
            ✕
          </button>
        </div>
      )}

      {/* Global Navbar */}
      <Navbar
        isLoggedIn={isLoggedIn}
        currentUser={currentUser}
        currentView={currentView}
        onOpenLogin={handleOpenLogin}
        onLogout={handleLogout}
        onNavigate={handleNavigateToView}
      />

      {/* Active Main View */}
      <div className="flex-1">
        {currentView === 'dashboard' ? (
          <Dashboard
            currentUser={currentUser}
            onBackToLanding={() => handleNavigateToView('landing')}
            onLogout={handleLogout}
            showToast={showToast}
          />
        ) : (
          <Home
            isLoggedIn={isLoggedIn}
            onGetStarted={isLoggedIn ? () => handleNavigateToView('dashboard') : handleOpenLogin}
            onViewDemo={handleDirectDemo}
            onOpenLogin={handleOpenLogin}
          />
        )}
      </div>

      {/* Footer */}
      <Footer onNavigate={handleNavigateToView} />

      {/* Login Modal */}
      <LoginModal
        isOpen={showLoginModal}
        onClose={handleCloseLogin}
        onLoginSuccess={handleLoginSuccess}
      />
    </div>
  );
}
