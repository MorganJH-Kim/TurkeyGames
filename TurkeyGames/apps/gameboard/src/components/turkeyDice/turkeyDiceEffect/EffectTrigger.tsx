import React from 'react';

interface EffectTriggerProps<T> {
  configs: T[]; // 이제 각 이펙트의 설정을 객체 배열로 받음
  EffectComponent: React.FC<T>;
}

function EffectTrigger<T>({ configs, EffectComponent }: EffectTriggerProps<T>) {
  return (
    <>
      {configs.map((props, idx) => (
        <EffectComponent key={idx} {...props} />
      ))}
    </>
  );
}

export default EffectTrigger;
