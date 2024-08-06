// C:\CHECKMESS\chessm-frontend\src\Spell.js

import React from 'react';

const Spell = ({ spell, onCast }) => (
  <div className="spell" onClick={() => onCast(spell)}>
    <p>{spell.type}</p>
  </div>
);

export default Spell;
