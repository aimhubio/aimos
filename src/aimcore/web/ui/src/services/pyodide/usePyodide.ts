import * as React from 'react';

import { loadPyodideInstance } from './pyodide';
import pyodideEngine, { usePyodideEngine } from './store';

function usePyodide() {
  const namespace = usePyodideEngine(pyodideEngine.pyodideNamespaceSelector);
  const pyodide = usePyodideEngine(pyodideEngine.pyodideCurrentSelector);
  const isLoading = usePyodideEngine(pyodideEngine.pyodideIsLoadingSelector);
  const registeredPackages = usePyodideEngine(
    pyodideEngine.pyodideRegisteredPackagesSelector,
  );
  const boards = usePyodideEngine(pyodideEngine.boardsSelector);
  const packages = usePyodideEngine(pyodideEngine.packagesSelector);

  const loadPyodide = React.useCallback(() => {
    if (pyodide !== null) {
      pyodide._api.fatal_error = async (err: unknown) => {
        // eslint-disable-next-line no-console
        console.log('---- fatal error ----', err);
        pyodideEngine.setPyodideCurrent(null);
      };
    }

    if (pyodide === null && isLoading === null) {
      loadPyodideInstance();
    }
  }, [pyodide, isLoading]);

  return {
    namespace,
    isLoading,
    registeredPackages,
    boards,
    packages,
    pyodide,
    loadPyodide,
  };
}

export default usePyodide;
