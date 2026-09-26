import React from 'react';
import cardGlowTr from '../assets/card-glow-tr.svg';
import cardGlowBl from '../assets/card-glow-bl.svg';

export default function ProcessCard({ step, title, description, icon }) {
  return (
    <article className="relative w-full max-w-[240px] xl:w-[190px] xl:h-[190px] min-h-[190px] rounded-[10px] p-4 flex flex-col items-center text-center card-new-glass group overflow-hidden">
      {/* Top-Right Ambient Amber Corner Glow from 02-NEW.svg */}
      <img
        src={cardGlowTr}
        alt=""
        aria-hidden="true"
        className="absolute -top-3 -right-3 w-16 h-16 pointer-events-none opacity-40 group-hover:opacity-75 transition-opacity"
      />

      {/* Bottom-Left Ambient Orange Corner Glow from 02-NEW.svg */}
      <img
        src={cardGlowBl}
        alt=""
        aria-hidden="true"
        className="absolute -bottom-3 -left-3 w-16 h-16 pointer-events-none opacity-40 group-hover:opacity-75 transition-opacity"
      />

      {/* Step Number Badge */}
      <div className="absolute top-2.5 left-3 text-[11px] font-mono font-bold tracking-wider text-tm-orange/80 bg-orange-50/80 px-1.5 py-0.5 rounded border border-tm-orange/20">
        {step}
      </div>

      {/* Process Icon */}
      <div className="w-10 h-10 flex items-center justify-center mt-1 mb-2">
        <img 
          src={icon} 
          alt="" 
          aria-hidden="true" 
          className="w-8 h-8 object-contain group-hover:scale-110 transition-transform duration-200" 
        />
      </div>

      {/* Step Title */}
      <h3 className="font-inter font-semibold text-[14px] text-tm-orange mb-1.5 leading-tight">
        {title}
      </h3>

      {/* Description */}
      <p className="font-inter font-normal text-[11.5px] leading-snug text-black/70 whitespace-pre-line mb-4 px-1">
        {description}
      </p>

      {/* Diagonal Arrow Circle */}
      <div className="absolute right-2.5 bottom-2.5 w-7 h-7 rounded-full border border-black/80 flex items-center justify-center text-[14px] text-black font-medium group-hover:bg-tm-orange group-hover:text-white group-hover:border-tm-orange transition-colors">
        ↗
      </div>
    </article>
  );
}
