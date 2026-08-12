'use client';

import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
}

export function Button({
  children,
  className,
  variant = 'primary',
  size = 'md',
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-brand-purple/40 disabled:opacity-50 disabled:cursor-not-allowed',
        size === 'sm' && 'px-2.5 py-1.5 text-xs',
        size === 'md' && 'px-4 py-2 text-sm',
        size === 'lg' && 'px-6 py-3 text-base',
        variant === 'primary' && 'bg-brand-purple text-white hover:bg-brand-purple/90',
        variant === 'secondary' && 'bg-surface-elevated text-text-primary border border-border hover:bg-surface-hover',
        variant === 'ghost' && 'bg-transparent text-text-secondary hover:bg-surface-hover hover:text-text-primary',
        variant === 'danger' && 'bg-status-offline/20 text-status-offline hover:bg-status-offline/30',
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;
