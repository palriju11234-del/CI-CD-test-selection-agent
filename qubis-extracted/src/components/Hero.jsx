import React from 'react';
import handRobotImage from '../assets/hero-hand-robot.png';
import robotImage from '../assets/qubis-robot.png';
import glowImage from '../assets/hero-glow.svg';

export default function Hero({ isLoggedIn, onGetStarted, onViewDemo }) {
  return (
    <section 
      id="home" 
      className="relative w-full min-h-[900px] overflow-hidden pt-[88px] lg:pt-0"
      style={{
        background: 'linear-gradient(116.5deg, #DAD7D7 0%, #F5F5F5 79.3%)'
      }}
    >
      {/* 1440x900 Desktop Canvas Container */}
      <div className="relative w-full max-w-[1440px] min-h-[900px] mx-auto">
        
        {/* Layer 1: Hand and Robotic Arm Artwork (Figma Node 3:3) */}
        <div 
          className="absolute inset-0 pointer-events-none z-10 hidden xl:block"
          aria-hidden="true"
        >
          <img
            src={handRobotImage}
            alt=""
            className="absolute object-contain pointer-events-none drop-shadow-[0_9px_6px_rgba(0,0,0,0.2)]"
            style={{
              width: '1552px',
              height: '1035px',
              left: '-120px',
              top: '192px',
              transform: 'rotate(-9.35deg)',
              transformOrigin: '0 0'
            }}
          />
        </div>

        {/* Tablet & Mobile Hero Artwork Container */}
        <div 
          className="xl:hidden relative w-full flex items-center justify-center my-6 z-10 pointer-events-none"
          aria-hidden="true"
        >
          <div className="relative w-[340px] sm:w-[480px] md:w-[600px] aspect-[4/3] flex items-center justify-center">
            {/* Ambient Glow */}
            <div className="absolute inset-0 flex items-center justify-center">
              <img src={glowImage} alt="" className="w-3/4 h-3/4 opacity-75 blur-xl" />
            </div>
            {/* Scaled Hands */}
            <img 
              src={handRobotImage} 
              alt="" 
              className="absolute inset-0 w-full h-full object-contain drop-shadow-md"
            />
            {/* Centered Robot */}
            <img 
              src={robotImage} 
              alt="QUBIS Robot" 
              className="relative w-[180px] sm:w-[220px] md:w-[260px] object-contain drop-shadow-[0_6px_5px_rgba(0,0,0,0.25)]"
            />
          </div>
        </div>

        {/* Layer 2: Orange Glow (Figma Node 4:25) - Desktop */}
        <div 
          className="hidden xl:block absolute z-20 pointer-events-none"
          style={{
            left: '548px',
            top: '412px',
            width: '286px',
            height: '296px'
          }}
          aria-hidden="true"
        >
          <img 
            src={glowImage} 
            alt="" 
            className="w-full h-full object-contain filter blur-[40px] opacity-80"
          />
        </div>

        {/* Layer 3: QUBIS Robot (Figma Node 3:6) - Desktop */}
        <div 
          className="hidden xl:block absolute z-30 pointer-events-none"
          style={{
            left: '494px',
            top: '377px',
            width: '412px',
            height: '412px'
          }}
        >
          <img
            src={robotImage}
            alt="QUBIS Robot Agent"
            className="w-full h-full object-contain drop-shadow-[0_6px_5px_rgba(0,0,0,0.25)]"
          />
        </div>

        {/* Top Left Text - Desktop: Left 119px, Top 139px */}
        <div className="relative xl:absolute xl:left-[119px] xl:top-[139px] z-40 px-6 xl:px-0 text-left max-w-xl xl:max-w-none">
          <h1 className="font-inter italic text-[28px] sm:text-[32px] xl:text-[36px] font-normal text-tm-orange leading-tight tracking-normal mb-4 xl:mb-6">
            Run the right tests.<br />Faster CI.
          </h1>
          <p className="font-inter font-light text-[18px] sm:text-[20px] xl:text-[24px] text-black leading-snug xl:w-[529px]">
            QUBIS is an AI-powered CI/CD agent that analyzes your code changes and selects only the relevant tests — reducing pipeline time, saving resources, and keeping your code safe.
          </p>
        </div>

        {/* Upper-Right Wordmark - Desktop: Left 870px, Top 139px */}
        <div 
          className="relative xl:absolute xl:left-[870px] xl:top-[139px] z-40 px-6 xl:px-0 text-left xl:text-left mt-6 xl:mt-0"
        >
          <h2 className="font-orbitron font-extrabold text-[44px] sm:text-[56px] xl:text-[70px] leading-none text-gradient-orbitron select-none tracking-tight">
            QUBIS
          </h2>
        </div>

        {/* Center Label below Robot - Desktop: Top 647px */}
        <div 
          className="relative xl:absolute xl:left-1/2 xl:-translate-x-1/2 xl:top-[647px] z-40 text-center px-4 mt-6 xl:mt-0"
        >
          <p className="font-inter font-light text-[20px] xl:text-[24px] text-black">
            CI/CD Test Selection Agent
          </p>
        </div>

        {/* Action Buttons - Desktop: Top 708px */}
        <div 
          className="relative xl:absolute xl:left-1/2 xl:-translate-x-1/2 xl:top-[708px] z-40 flex flex-col sm:flex-row items-center justify-center gap-4 xl:gap-[20px] px-6 mt-6 xl:mt-0"
        >
          <button
            type="button"
            onClick={onGetStarted}
            className="btn-get-started w-[235px] h-[74px] rounded-[50px] flex items-center justify-center font-inter font-medium text-[22px] xl:text-[24px] text-black tracking-normal cursor-pointer select-none"
            aria-label="Get Started with QUBIS"
          >
            {isLoggedIn ? 'Go to Dashboard' : 'Get Started'}
          </button>
          <button
            type="button"
            onClick={onViewDemo}
            className="btn-view-demo w-[235px] h-[74px] rounded-[50px] flex items-center justify-center font-inter font-medium text-[22px] xl:text-[24px] text-black tracking-normal cursor-pointer select-none"
            aria-label="View Live Interactive Demo"
          >
            View Demo
          </button>
        </div>

        {/* Footer Text - Desktop: Top 829px */}
        <div 
          className="relative xl:absolute xl:left-1/2 xl:-translate-x-1/2 xl:top-[829px] z-40 text-center px-4 pb-12 xl:pb-0 mt-6 xl:mt-0"
        >
          <p className="font-inter font-medium text-[13px] xl:text-[14px] text-tm-muted">
            Works with GitHub, GitLab, Jenkins and more
          </p>
        </div>

      </div>
    </section>
  );
}
