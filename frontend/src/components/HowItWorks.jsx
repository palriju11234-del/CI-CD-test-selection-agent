import React from 'react';
import ProcessCard from './ProcessCard.jsx';
import howItWorksBg from '../assets/how-it-works-bg.svg';

import codePushIcon from '../assets/icons/code-push.svg';
import githubWebhookIcon from '../assets/icons/github-webhook.svg';
import aiAnalysisIcon from '../assets/icons/ai-analysis.svg';
import selectTestIcon from '../assets/icons/select-test.svg';
import runCiIcon from '../assets/icons/run-ci.svg';

export default function HowItWorks() {
  const steps = [
    {
      step: '01',
      title: 'Code Push',
      description: 'Developer pushes\ncode or creates a\npull request',
      icon: codePushIcon,
    },
    {
      step: '02',
      title: 'GitHub Webhook',
      description: 'Triggers the\nQUBIS\nagent',
      icon: githubWebhookIcon,
    },
    {
      step: '03',
      title: 'AI Analysis',
      description: '-Changes files\n-Dependencies\n-Historic CI data',
      icon: aiAnalysisIcon,
    },
    {
      step: '04',
      title: 'Select Relevant Test',
      description: 'Predicts and selects\nonly the necessary\ntests',
      icon: selectTestIcon,
    },
    {
      step: '05',
      title: 'Run in CI',
      description: 'Executes selected\ntests via GitHub\naction',
      icon: runCiIcon,
    },
  ];

  return (
    <section 
      id="how-it-works" 
      className="relative w-full py-20 lg:py-28 overflow-hidden bg-cover bg-center bg-no-repeat"
      style={{
        backgroundImage: `url(${howItWorksBg})`
      }}
    >
      <div className="max-w-[1340px] mx-auto px-6 relative z-10">
        {/* Section Heading */}
        <div className="text-center mb-14 lg:mb-20">
          <h2 className="font-inter font-normal text-[40px] sm:text-[50px] lg:text-[64px] text-black tracking-tight leading-tight mb-3">
            How It Works?
          </h2>
          <p className="font-inter font-normal text-[18px] sm:text-[20px] text-tm-orange">
            From code change to test results all automated
          </p>
        </div>

        {/* 5-Step Pipeline Grid with desktop horizontal flow & subtle connectors */}
        <div className="flex flex-col md:flex-row flex-wrap xl:flex-nowrap items-center justify-center gap-6 xl:gap-5 max-w-[1280px] mx-auto">
          {steps.map((item, idx) => (
            <React.Fragment key={item.step}>
              <ProcessCard
                step={item.step}
                title={item.title}
                description={item.description}
                icon={item.icon}
              />
              {/* Subtle horizontal arrow indicator between cards on desktop */}
              {idx < steps.length - 1 && (
                <div 
                  className="hidden xl:flex items-center justify-center text-tm-orange/40 text-lg select-none px-1"
                  aria-hidden="true"
                >
                  <svg className="w-5 h-5 text-tm-orange/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              )}
            </React.Fragment>
          ))}
        </div>
      </div>
    </section>
  );
}
