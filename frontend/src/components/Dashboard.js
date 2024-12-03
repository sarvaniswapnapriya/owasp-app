import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [username, setUsername] = useState('');
  const [gameState, setGameState] = useState({
    cards: [],
    flippedCards: [],
    matchedCards: [],
    score: 0,
  });

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user_data'));
    setUsername(userData?.username || 'Player');
    initializeGame();
  }, []);

  const initializeGame = () => {
    const cardSet = ['💀', '🫣', '🥱', '🚀', '🗿', '🤡'];
    const shuffledCards = [...cardSet, ...cardSet]
      .sort(() => 0.5 - Math.random())
      .map((card, index) => ({ id: index, value: card, flipped: false }));

    setGameState((prev) => ({ ...prev, cards: shuffledCards, score: 0 }));
  };

  const handleCardClick = (card) => {
    if (gameState.flippedCards.length < 2 && !card.flipped) {
      const updatedCards = gameState.cards.map((c) =>
        c.id === card.id ? { ...c, flipped: true } : c
      );
      const updatedFlippedCards = [...gameState.flippedCards, card];

      setGameState((prev) => ({
        ...prev,
        cards: updatedCards,
        flippedCards: updatedFlippedCards,
      }));

      if (updatedFlippedCards.length === 2) {
        setTimeout(() => checkForMatch(updatedFlippedCards), 800);
      }
    }
  };

  const checkForMatch = (flippedCards) => {
    const [card1, card2] = flippedCards;
    let updatedCards = [...gameState.cards];

    if (card1.value === card2.value) {
      updatedCards = updatedCards.map((card) =>
        card.id === card1.id || card.id === card2.id
          ? { ...card, matched: true }
          : card
      );
      setGameState((prev) => ({
        ...prev,
        score: prev.score + 10,
        matchedCards: [...prev.matchedCards, card1.value],
      }));
    } else {
      updatedCards = updatedCards.map((card) =>
        card.id === card1.id || card.id === card2.id
          ? { ...card, flipped: false }
          : card
      );
    }

    setGameState((prev) => ({
      ...prev,
      cards: updatedCards,
      flippedCards: [],
    }));
  };

  const resetGame = () => {
    initializeGame();
  };

  return (
    <div className="dashboard" style={{ textAlign: 'center', padding: '20px' }}>
      <h1 style={{ marginBottom: '20px' }}>
        Welcome back, {username}! Let's play a matching game!
      </h1>
      <div style={{ fontSize: '20px', marginBottom: '20px' }}>Score: {gameState.score}</div>

      <div
        className="game-grid"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 100px)',
          gap: '10px',
          justifyContent: 'center',
        }}
      >
        {gameState.cards.map((card) => (
          <div
            key={card.id}
            onClick={() => handleCardClick(card)}
            style={{
              width: '100px',
              height: '100px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: card.flipped || card.matched ? '#4a90e2' : '#ccc',
              border: '2px solid #333',
              color: '#fff',
              fontSize: '3rem', // Adjusted to fit emoji size
              cursor: card.flipped || card.matched ? 'default' : 'pointer',
              borderRadius: '8px',
              transition: 'transform 0.3s',
              transform: card.flipped ? 'scale(1.1)' : 'scale(1)',
            }}
          >
            {card.flipped || card.matched ? card.value : ''}
          </div>
        ))}
      </div>

      <button
        onClick={resetGame}
        style={{
          marginTop: '20px',
          padding: '10px 20px',
          backgroundColor: '#28a745',
          color: '#fff',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        Restart Game
      </button>
    </div>
  );
}

export default Dashboard;
