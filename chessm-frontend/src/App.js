import React, { useState, useEffect } from 'react';
import Board from './Board';
import './styles.css';

const App = () => {
  const [gameId, setGameId] = useState(null);
  const [boardState, setBoardState] = useState('');
  const [spells, setSpells] = useState([]);

  useEffect(() => {
    const startNewGame = async () => {
      const response = await fetch('http://127.0.0.1:5000/api/new_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const result = await response.json();
      if (result.game_id) {
        setGameId(result.game_id);
        setBoardState(result.board_state);
      }
    };
    startNewGame();
  }, []);

  const handleMove = async (from, to) => {
    const move = `${from}-${to}`;
    const response = await fetch('http://127.0.0.1:5000/api/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ game_id: gameId, move: move }),
    });
    const result = await response.json();
    if (result.board_state) {
      setBoardState(result.board_state);
    } else {
      alert(result.error);
    }
  };

  const castSpell = async (spellId, targetPiece) => {
    const response = await fetch('http://127.0.0.1:5000/api/cast_spell', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ game_id: gameId, spell_id: spellId, target_piece: targetPiece }),
    });
    const result = await response.json();
    if (result.board_state) {
      setBoardState(result.board_state);
      // Update spell state or UI accordingly
      setSpells([...spells, { id: spellId, target_piece: targetPiece }]); // Example update
    } else {
      alert(result.error);
    }
  };

  return (
    <div>
      <h1>Welcome to CheckMess Frontend!</h1>
      <Board boardState={boardState} onMove={handleMove} spells={spells} />
      <button onClick={() => castSpell(1, 'P')}>Cast Spell 1</button>
      <button onClick={() => castSpell(2, ' ')}>Cast Spell 2</button>
    </div>
  );
};

export default App;
