import React, { useState } from 'react';
import '../styles/LeaderboardPage.css';

const Leaderboards = () => {
  const leaderboardData = [
    { rank: 1, name: 'Alice', score: 1200 },
    { rank: 2, name: 'Bob', score: 1100 },
    { rank: 3, name: 'Charlie', score: 1050 },
    { rank: 4, name: 'Diana', score: 1000 },
    { rank: 5, name: 'Eve', score: 950 },
  ];

  const leaderboards = [
    { title: 'Top 5 Overall', data: leaderboardData },
    { title: 'Top 5 Steps', data: leaderboardData },
    { title: 'Top 5 Active Days', data: leaderboardData },
    { title: 'Top 5 Challenges', data: leaderboardData },
  ];

  const [filters, setFilters] = useState(leaderboards.map(() => 'All Time'));

  const handleFilterChange = (e, index) => {
    const selectedFilter = e.target.value;
    const updatedFilters = [...filters];
    updatedFilters[index] = selectedFilter;
    setFilters(updatedFilters);
  };

  return (
    <main className="leaderboards-page">
      <div className="leaderboards-container">
        <h2>Leaderboards</h2>
        <p>See where you rank among others! Here's the current leaderboard:</p>
        <div className="leaderboards-grid">
          {leaderboards.map((leaderboard, index) => (
            <div className="leaderboard-card" key={index}>
              <div className="leaderboard-header">
                <h3>{leaderboard.title}</h3>
                <select
                  value={filters[index]}
                  onChange={(e) => handleFilterChange(e, index)}
                  className="filter-dropdown"
                >
                  <option value="All Time">All Time</option>
                  <option value="Week">Week</option>
                  <option value="Month">Month</option>
                  <option value="Year">Year</option>
                </select>
              </div>
              <table className="leaderboard-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Name</th>
                    <th>Score</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.data.map((user) => (
                    <tr key={user.rank}>
                      <td>
                        <span className={`rank-badge rank-${user.rank}`}>
                          {user.rank}
                        </span>
                      </td>
                      <td>{user.name}</td>
                      <td>{user.score}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
};

export default Leaderboards;
