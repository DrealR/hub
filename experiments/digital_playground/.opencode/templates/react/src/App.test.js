import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders project name', () => {
  render(<App />);
  const heading = screen.getByRole('heading', { name: /{{PROJECT_NAME}}/i });
  expect(heading).toBeInTheDocument();
});