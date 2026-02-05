// Tests for {{PROJECT_NAME}}
const { main } = require('./index');

describe('{{PROJECT_NAME}}', () => {
  test('should export main function', () => {
    expect(typeof main).toBe('function');
  });
  
  test('main should not throw', () => {
    expect(() => main()).not.toThrow();
  });
});
