// Game.js
import React, { useState, useEffect } from 'react';
import Board from './Board';

const Game = () => {
  const [boardState, setBoardState] = useState(null);
  const [gameId, setGameId] = useState(null);
  const [spells, setSpells] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/new_game', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        setGameId(data.game_id);
        setBoardState(data.board_state);
      });
  }, []);

  const handleMove = (fromSquare, toSquare) => {
    fetch('http://127.0.0.1:5000/api/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ game_id: gameId, from_square: fromSquare, to_square: toSquare })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setBoardState(data.board_state);
      })
      .catch(error => {
        console.error('Error making move:', error);
        alert('Failed to make move. Please try again.');
      });
  };

  return (
    <div>
      <h1>Welcome to CheckMess Frontend!</h1>
      {boardState ? (
        <Board boardState={boardState} onMove={handleMove} spells={spells} />
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Game;
