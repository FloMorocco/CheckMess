import React, { useState } from 'react';

const Board = ({ boardState, onMove }) => {
  const [selectedSquare, setSelectedSquare] = useState(null);

  const handleSquareClick = (index) => {
    if (selectedSquare === null) {
      setSelectedSquare(index);
    } else {
      onMove(selectedSquare, index);
      setSelectedSquare(null);
    }
  };

  const renderSquare = (piece, index) => {
    const isWhite = (Math.floor(index / 8) + index) % 2 === 0;
    const isSelected = selectedSquare === index;
    return (
      <div
        key={index}
        className={`square ${isWhite ? 'white-square' : 'black-square'} ${isSelected ? 'selected-square' : ''}`}
        onClick={() => handleSquareClick(index)}
      >
        {piece !== ' ' ? piece : null}
      </div>
    );
  };

  const renderBoard = () => {
    if (!boardState) return null;
    const squares = [];
    let index = 0;

    for (let row of boardState.split('/')) {
      for (let char of row) {
        if (char === ' ') {
          squares.push(renderSquare(' ', index++));
        } else {
          squares.push(renderSquare(char, index++));
        }
      }
    }

    return <div className="board-grid">{squares}</div>;
  };

  return <div className="board">{renderBoard()}</div>;
};

export default Board;
