import React from 'react';
import styles from './Default.module.css';
import turkey from '../../assets/images/turkey.png';
import SpinTurkey from '../../components/common/spinTurkey/SpinTurkey';
import EffectAnimation from '../../components/turkeyDice/turkeyDiceEffect/StarEffectAnimation';
import EffectTrigger from '../../components/turkeyDice/turkeyDiceEffect/EffectTrigger';
import HeartEffectAnimation from '../../components/turkeyDice/turkeyDiceEffect/HeartEffectAnimation';
import StarEffectAnimation from '../../components/turkeyDice/turkeyDiceEffect/StarEffectAnimation';
import ExplosionEffectAnimation from '../../components/turkeyDice/turkeyDiceEffect/ExplosionEffectAnimation';
import ThunderEffectAnimation from '../../components/turkeyDice/turkeyDiceEffect/ThunderEffectAnimation';
import BulletImpactEffect from '../../components/turkeyDice/turkeyDiceEffect/BulletImpactEffect';

export default function Default() {
  const starConfigs = [
    { x: 200, y: 240, withSound: true },
    { x: 400, y: 450, withSound: false },
    { x: 600, y: 550, withSound: true },
    { x: 800, y: 350, withSound: false },
    { x: 600, y: 650, withSound: true },
  ];

  return (
    <div className={styles.layout}>
      <SpinTurkey image={turkey} />
      <HeartEffectAnimation />
      <StarEffectAnimation />
      <ExplosionEffectAnimation />
      <ThunderEffectAnimation />
    </div>
  );
}
