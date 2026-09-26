import React from 'react';
import Hero from '../components/Hero.jsx';
import HowItWorks from '../components/HowItWorks.jsx';
import Features from '../components/Features.jsx';
import Docs from '../components/Docs.jsx';
import Login from '../components/Login.jsx';

export default function Home({ isLoggedIn, onGetStarted, onViewDemo, onOpenLogin }) {
  return (
    <main>
      <Hero
        isLoggedIn={isLoggedIn}
        onGetStarted={onGetStarted}
        onViewDemo={onViewDemo}
      />
      <HowItWorks />
      <Features />
      <Docs onOpenLogin={onOpenLogin} onViewDemo={onViewDemo} />
      <Login
        isLoggedIn={isLoggedIn}
        onOpenLogin={onOpenLogin}
        onViewDemo={onViewDemo}
      />
    </main>
  );
}
