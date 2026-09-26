import React from 'react';
import FeatureCard from './FeatureCard.jsx';
import featuresBg from '../assets/features-bg.svg';

import codeChangeIcon from '../assets/icons/code-change.svg';
import dependencyIcon from '../assets/icons/dependency-mapping.svg';
import rlIcon from '../assets/icons/reinforcement-learning.svg';
import safeIcon from '../assets/icons/safe-reliable.svg';
import integrationIcon from '../assets/icons/seamless-integration.svg';

export default function Features() {
  const featureList = [
    {
      title: 'Code change analysis',
      description: 'Understands what changes, where and why',
      icon: codeChangeIcon,
    },
    {
      title: 'Dependency Mapping',
      description: 'Finds relevant modules, service and test',
      icon: dependencyIcon,
    },
    {
      title: 'Reinforcement Learning',
      description: 'Learns from historic CI data to predict test relevance',
      icon: rlIcon,
    },
    {
      title: 'Safe & Reliable',
      description: 'Maintains high accuracy and avoids false negatives',
      icon: safeIcon,
    },
    {
      title: 'Seamless Integration',
      description: 'Works with GitHub, GitLab, Jenkins and more',
      icon: integrationIcon,
    },
  ];

  return (
    <section 
      id="features" 
      className="relative w-full py-20 lg:py-28 overflow-hidden bg-cover bg-center bg-no-repeat"
      style={{
        backgroundImage: `url(${featuresBg})`
      }}
    >
      <div className="max-w-[1340px] mx-auto px-6 relative z-10">
        {/* Feature Top Split Banner */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-16 items-start mb-16 max-w-[1290px] mx-auto">
          <div className="lg:col-span-7">
            <h2 className="font-inter text-[32px] sm:text-[36px] xl:text-[40px] text-black leading-tight mb-2">
              <span className="font-bold">Smarter</span>{' '}
              <span className="text-tm-orange font-normal">Test Selection.</span>
            </h2>
            <p className="font-inter italic text-[16px] sm:text-[18px] text-black/75">
              Build for Modern Development.
            </p>
          </div>
          <div className="lg:col-span-5">
            <p className="font-inter font-light text-[17px] sm:text-[18px] text-black leading-relaxed">
              QUBIS learns from your codebase and CI history to predict which tests matter, so you can ship faster without compromising quality.
            </p>
          </div>
        </div>

        {/* Section Subheading */}
        <div className="max-w-[1290px] mx-auto mb-10">
          <h3 className="font-inter font-normal text-[26px] sm:text-[30px] text-tm-orange">
            Features
          </h3>
        </div>

        {/* 5 Feature Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-6 xl:gap-8 justify-items-center max-w-[1290px] mx-auto">
          {featureList.map((item) => (
            <FeatureCard
              key={item.title}
              title={item.title}
              description={item.description}
              icon={item.icon}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
