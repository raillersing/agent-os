'use client';

import { Modal } from './Modal';
import { Button } from './Button';

interface GenerateMediaModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: 'image' | 'video' | 'speech';
}

export function GenerateMediaModal({ isOpen, onClose, type }: GenerateMediaModalProps) {
  const title = type.charAt(0).toUpperCase() + type.slice(1);

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Generate ${title}`}>
      <div className="space-y-4">
        {type === 'image' && (
          <>
            <div>
              <label className="mb-1 block text-xs font-medium text-text-secondary">Prompt</label>
              <textarea
                rows={3}
                placeholder="Describe the image you want to generate..."
                className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary outline-none placeholder:text-text-muted focus:border-brand-purple"
              />
            </div>
            <div>
              <label className="mb-1 block text-xs font-medium text-text-secondary">Aspect Ratio</label>
              <select className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary outline-none">
                <option>1:1</option>
                <option>16:9</option>
                <option>9:16</option>
                <option>4:3</option>
              </select>
            </div>
          </>
        )}

        {type === 'video' && (
          <>
            <div>
              <label className="mb-1 block text-xs font-medium text-text-secondary">Prompt</label>
              <textarea
                rows={3}
                placeholder="Describe the video scene..."
                className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary outline-none placeholder:text-text-muted focus:border-brand-purple"
              />
            </div>
            <div>
              <label className="mb-1 block text-xs font-medium text-text-secondary">Duration</label>
              <select className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary outline-none">
                <option>5 seconds</option>
                <option>10 seconds</option>
                <option>30 seconds</option>
                <option>60 seconds</option>
              </select>
            </div>
          </>
        )}

        {type === 'speech' && (
          <>
            <div>
              <label className="mb-1 block text-xs font-medium text-text-secondary">Text</label>
              <textarea
                rows={3}
                placeholder="Enter the text to synthesize..."
                className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary outline-none placeholder:text-text-muted focus:border-brand-purple"
              />
            </div>
            <div>
              <label className="mb-1 block text-xs font-medium text-text-secondary">Voice</label>
              <select className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary outline-none">
                <option>Nova</option>
                <option>Onyx</option>
                <option>Echo</option>
                <option>Alloy</option>
              </select>
            </div>
          </>
        )}

        <div className="flex justify-end gap-2 pt-2">
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button variant="primary">Generate {title}</Button>
        </div>
      </div>
    </Modal>
  );
}
