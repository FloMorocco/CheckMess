import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import './App.css';

const socket = io('http://127.0.0.1:5000');

const Chessboard = () => {
    const [board, setBoard] = useState(null);
    const [selectedSquare, setSelectedSquare] = useState(null);

    useEffect(() => {
        fetch('http://127.0.0.1:5000/api/board?game_id=1')
            .then(response => response.json())
            .then(data => setBoard(data.board_state))  // Updated key to match backend response
            .catch(error => console.error('Error fetching board data:', error));

        socket.emit('join', { game_id: '1' });

        socket.on('move', data => {
            if (data.success) {
                setBoard(data.board);
            }
        });

        return () => {
            socket.emit('leave', { game_id: '1' });
        };
    }, []);

    const handleSquareClick = (row, col) => {
        const currentSquare = `${String.fromCharCode(97 + col)}${8 - row}`;
        console.log('Square clicked:', currentSquare);
        if (selectedSquare) {
            const move = `${selectedSquare}${currentSquare}`;
            console.log('Move attempted:', move);
            fetch('http://127.0.0.1:5000/api/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ game_id: '1', move }),
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Move response:', data);
                    if (data.success) {
                        setBoard(data.board);
                        socket.emit('move', { game_id: '1', move });
                        setSelectedSquare(null);
                    } else {
                        console.error('Invalid move:', data.message);
                        setSelectedSquare(null);
                    }
                })
                .catch(error => {
                    console.error('Error making move:', error);
                    setSelectedSquare(null);
                });
        } else {
            setSelectedSquare(currentSquare);
        }
    };

    const renderSquare = (square, row, col) => {
        const pieceSymbols = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
        };
        const currentSquare = `${String.fromCharCode(97 + col)}${8 - row}`;
        return (
            <div
                key={col}
                className={`square ${selectedSquare === currentSquare ? 'selected' : ''}`}
                onClick={() => handleSquareClick(row, col)}
            >
                {pieceSymbols[square] || ''}
            </div>
        );
    };

    const renderBoard = () => {
        if (!board) return <p>Loading board...</p>;
        const rows = board.split(' ')[0].split('/');
        return rows.map((row, i) => (
            <div key={i} className="row">
                {row.split('').map((square, j) => {
                    if (/\d/.test(square)) {
                        return [...Array(parseInt(square))].map((_, k) => (
                            <div key={j + k} className="square"></div>
                        ));
                    }
                    return renderSquare(square, i, j);
                })}
            </div>
        ));
    };

    return (
        <div className="chessboard">
            {renderBoard()}
        </div>
    );
};

export default Chessboard;
