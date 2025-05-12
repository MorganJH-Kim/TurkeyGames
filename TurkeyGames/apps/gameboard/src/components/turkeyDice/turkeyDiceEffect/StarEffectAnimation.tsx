// src/components/turkeyDice/turkeyDiceEffect/EffectAnimation.tsx

import React, { useEffect } from 'react';

const frameCount = 23;
const frameDuration = 50;
const startFrameIndex = 0;

const framePaths = Array.from(
  { length: frameCount },
  (_, i) =>
    new URL(
      `../../../assets/effects/star/Fx02_${String(i + startFrameIndex).padStart(
        2,
        '0'
      )}.png`,
      import.meta.url
    ).href
);

// ⭐ 하드코딩된 이펙트 좌표
const hardcodedPositions = [
  { x: 200, y: 240 },
  { x: 400, y: 450 },
  { x: 600, y: 550 },
  { x: 800, y: 350 },
  { x: 600, y: 650 },
];

const StarEffectAnimation: React.FC = () => {
  useEffect(() => {
    // 효과음 재생 (필요 시 사운드 파일 경로 수정 가능)
    const audio = new Audio('/sounds/twinkle.mp3');
    audio.play().catch((err) => console.warn('🎵 사운드 재생 실패:', err));

    hardcodedPositions.forEach(({ x, y }) => {
      let current = 0;
      const img = document.createElement('img');

      Object.assign(img.style, {
        position: 'absolute',
        left: `${x}px`,
        top: `${y}px`,
        transform: 'translate(-50%, -50%) scale(1.2)',
        pointerEvents: 'none',
        width: '150px',
        height: '150px',
        zIndex: '999',
        border: 'none',
        outline: 'none',
        background: 'transparent',
        mixBlendMode: 'screen',
      });

      document.body.appendChild(img);

      const interval = setInterval(() => {
        if (current >= framePaths.length) {
          clearInterval(interval);
          img.remove();
        } else {
          img.src = framePaths[current];
          current++;
        }
      }, frameDuration);
    });
  }, []);

  return null;
};

export default StarEffectAnimation;
