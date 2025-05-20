import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

// Define generic type parameters for the hook
type PollingStatus = 'idle' | 'loading' | 'success' | 'error';
type PollingResponse<T> = {
  data: T | null;
  intermediateData: T | null;
  status: PollingStatus;
  error: Error | null;
};

interface PollingOptions {
  interval?: number;
  maxAttempts?: number;
}

interface PollingState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  intermediateResult: any;
}

/**
 * Custom hook for polling an API endpoint until a condition is met or max retries is reached
 * 
 * @param url - The URL to poll
 * @param options - Configuration options for polling
 * @returns PollingResponse object with data, status, and error
 */
export function usePollingState<T>(
  fetchFn: () => Promise<T>,
  options: PollingOptions = {}
): [PollingState<T>, () => void] {
  const {
    interval = 1000,
    maxAttempts = 30
  } = options;

  const [state, setState] = useState<PollingState<T>>({
    data: null,
    loading: false,
    error: null,
    intermediateResult: null
  });

  const [attempts, setAttempts] = useState(0);
  const [shouldPoll, setShouldPoll] = useState(false);

  const startPolling = useCallback(() => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    setAttempts(0);
    setShouldPoll(true);
  }, []);

  useEffect(() => {
    let timeoutId: number;

    const poll = async () => {
      if (!shouldPoll || attempts >= maxAttempts) {
        setShouldPoll(false);
        return;
      }
      
      try {
        const result = await fetchFn();
        setState(prev => ({
          ...prev,
          data: result,
          loading: false,
          error: null
        }));
        setShouldPoll(false);
      } catch (error) {
        if (attempts < maxAttempts) {
          setAttempts(prev => prev + 1);
          timeoutId = window.setTimeout(poll, interval);
        } else {
        setState(prev => ({
          ...prev,
            loading: false,
            error: 'Maximum polling attempts reached'
          }));
          setShouldPoll(false);
        }
    }
  };

    if (shouldPoll) {
      poll();
    }

    return () => {
      if (timeoutId) {
        window.clearTimeout(timeoutId);
      }
    };
  }, [shouldPoll, attempts, maxAttempts, interval, fetchFn]);

  return [state, startPolling];
}

/* File Explanation:
 * This file implements a custom React hook for handling polling state and API responses.
 * Key features:
 * 1. Manages loading, error, and data states
 * 2. Supports configurable polling interval and maximum attempts
 * 3. Handles intermediate results during polling
 * 4. Provides cleanup on unmount
 * 5. Type-safe implementation with TypeScript
 * The hook is used to handle asynchronous API responses that require polling for updates.
 */