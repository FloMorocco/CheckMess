// Spell.js
import React from 'react';

const Spell = ({ name, onClick }) => {
  return (
    <button onClick={onClick}>
      {name}
    </button>
  );
};

export default Spell;
