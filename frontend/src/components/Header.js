import React from 'react';

const Header = ({ user, onLogout }) => {
  return (
    <header className="header">
      <h1>Privacy Analytics Platform</h1>
      <div className="header-user">
        <div className="user-info">
          <div className="user-name">{user?.full_name || user?.username}</div>
          <div className="user-role">{user?.role?.toUpperCase()}</div>
        </div>
        <button className="logout-btn" onClick={onLogout}>
          Logout
        </button>
      </div>
    </header>
  );
};

export default Header; 