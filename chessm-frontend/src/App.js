import React, { useState, useEffect } from 'react';
import Board from './Board';
import Spell from './Spell';

const App = () => {
  const [gameId, setGameId] = useState(null);
  const [boardState, setBoardState] = useState('');
  const [spells, setSpells] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/new_game', {
      method: 'POST',
    })
      .then(response => response.json())
      .then(data => {
        setGameId(data.game_id);
        setBoardState(data.board_state);
      });
  }, []);

  const handleMove = (from, to) => {
    fetch('http://127.0.0.1:5000/api/move', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        game_id: gameId,
        move: `${from}-${to}`,
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.board_state) {
          setBoardState(data.board_state);
        } else {
          console.error('Invalid move');
        }
      })
      .catch(error => console.error('Error:', error));
  };

  const castSpell = (spellId) => {
    fetch('http://127.0.0.1:5000/api/cast_spell', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        game_id: gameId,
        spell_id: spellId,
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setSpells(data.active_spells);
        } else {
          console.error('Failed to cast spell');
        }
      })
      .catch(error => console.error('Error:', error));
  };

  return (
    <div>
      <h1>Welcome to CheckMess Frontend!</h1>
      <Board boardState={boardState} onMove={handleMove} />
      <div>
        <button onClick={() => castSpell(1)}>Cast Spell 1</button>
        <button onClick={() => castSpell(2)}>Cast Spell 2</button>
      </div>
    </div>
  );
};

export default App;
