import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="contact-info">
        <p>Контактная информация: example@example.com | +123 456 7890</p>
      </div>
      <div className="agreement-link">
        <a href="https://www.youtube.com" target="_blank" rel="noopener noreferrer">Пользовательское соглашение</a>
      </div>
    </footer>
  );
};

export default Footer;