import React from 'react';

export default function Docs({ onOpenLogin, onViewDemo }) {
  const steps = [
    {
      num: '1',
      title: 'Repository',
      subtitle: 'Connect GitHub / GitLab webhook',
    },
    {
      num: '2',
      title: 'Analysis',
      subtitle: 'Detect changed code, AST graph & dependencies',
    },
    {
      num: '3',
      title: 'Execution',
      subtitle: 'Run only relevant tests in CI pipeline',
    },
  ];

  return (
    <section 
      id="docs" 
      className="relative w-full py-20 lg:py-28 overflow-hidden"
      style={{
        background: 'linear-gradient(120deg, #DAD7D7 0%, #FFFFFF 100%)'
      }}
    >
      <div className="max-w-[1290px] mx-auto px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          {/* Left Text */}
          <div>
            <p className="text-tm-orange font-semibold text-[13px] tracking-[0.16em] uppercase mb-3">
              DOCUMENTATION & INTEGRATION
            </p>
            <h2 className="font-inter text-[36px] sm:text-[42px] xl:text-[46px] text-black font-normal leading-[1.1] mb-6">
              Connect your repository.<br />Let QUBIS handle the selection.
            </h2>
            <p className="font-inter font-light text-[17px] sm:text-[18px] text-black/75 leading-relaxed max-w-[540px] mb-8">
              Start with a GitHub webhook, inspect the selected test set, and plug the result into your existing CI pipeline with zero complex setup.
            </p>

            <div className="flex items-center gap-4">
              <button
                type="button"
                onClick={onViewDemo}
                className="btn-get-started px-6 h-[54px] rounded-[50px] font-inter font-medium text-[16px] text-black flex items-center gap-2 cursor-pointer hover:scale-105 transition-transform"
              >
                <span>View Sample PR Pipeline</span>
                <span>→</span>
              </button>
            </div>
          </div>

          {/* Right Panel Cards */}
          <div className="flex flex-col gap-4 max-w-[500px] w-full">
            {steps.map((step) => (
              <div 
                key={step.num}
                className="grid grid-cols-[44px_1fr] gap-4 items-center p-5 rounded-[18px] card-new-glass border border-[#DAD7D7]"
              >
                <div className="w-[38px] h-[38px] rounded-full border border-black/40 bg-white/60 flex items-center justify-center font-inter font-bold text-[16px] text-black shadow-sm">
                  {step.num}
                </div>
                <div>
                  <b className="block text-[16px] text-tm-orange font-semibold">
                    {step.title}
                  </b>
                  <span className="block text-[14px] text-black/70 mt-0.5">
                    {step.subtitle}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
