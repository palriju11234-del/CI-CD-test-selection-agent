import React from 'react';
import cardGlowTr from '../assets/card-glow-tr.svg';
import cardGlowBl from '../assets/card-glow-bl.svg';

export default function FeatureCard({ icon, title, description }) {
  return (
    <article className="relative w-full max-w-[240px] xl:w-[213px] xl:h-[213px] min-h-[213px] rounded-[14px] p-5 flex flex-col items-center text-center card-new-glass group overflow-hidden">
      {/* Top-Right Ambient Amber Corner Glow from 03-NEW.svg */}
      <img
        src={cardGlowTr}
        alt=""
        aria-hidden="true"
        className="absolute -top-4 -right-4 w-18 h-18 pointer-events-none opacity-40 group-hover:opacity-75 transition-opacity"
      />

      {/* Bottom-Left Ambient Orange Corner Glow from 03-NEW.svg */}
      <img
        src={cardGlowBl}
        alt=""
        aria-hidden="true"
        className="absolute -bottom-4 -left-4 w-18 h-18 pointer-events-none opacity-40 group-hover:opacity-75 transition-opacity"
      />

      {/* Feature Icon */}
      <div className="w-12 h-12 flex items-center justify-center mb-3">
        <img 
          src={icon} 
          alt="" 
          aria-hidden="true" 
          className="w-9 h-9 object-contain group-hover:scale-110 transition-transform duration-200" 
        />
      </div>

      {/* Feature Title */}
      <h3 className="font-inter font-semibold text-[14px] text-tm-orange mb-2 leading-tight">
        {title}
      </h3>

      {/* Description */}
      <p className="font-inter font-normal text-[12.5px] leading-snug text-black/70 max-w-[155px]">
        {description}
      </p>
    </article>
  );
}
