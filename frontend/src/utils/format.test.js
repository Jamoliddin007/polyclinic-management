import { describe, it, expect } from 'vitest';
import {
  formatMoney, paymentStatusLabel, paymentStatusColor, genderLabel,
} from './format.js';

describe('formatMoney', () => {
  it('formats with so\'m suffix', () => {
    expect(formatMoney(100000)).toContain("so'm");
  });

  it('returns dash for null', () => {
    expect(formatMoney(null)).toBe('—');
  });

  it('returns dash for undefined', () => {
    expect(formatMoney(undefined)).toBe('—');
  });
});

describe('paymentStatusLabel', () => {
  it('translates PAID', () => {
    expect(paymentStatusLabel('PAID')).toBe("To'langan");
  });

  it('translates PENDING', () => {
    expect(paymentStatusLabel('PENDING')).toBe('Kutilmoqda');
  });

  it('falls back to original value', () => {
    expect(paymentStatusLabel('UNKNOWN')).toBe('UNKNOWN');
  });
});

describe('paymentStatusColor', () => {
  it('returns green for PAID', () => {
    expect(paymentStatusColor('PAID')).toContain('green');
  });

  it('returns red for CANCELLED', () => {
    expect(paymentStatusColor('CANCELLED')).toContain('red');
  });
});

describe('genderLabel', () => {
  it('translates M to Erkak', () => {
    expect(genderLabel('M')).toBe('Erkak');
  });

  it('translates F to Ayol', () => {
    expect(genderLabel('F')).toBe('Ayol');
  });
});
