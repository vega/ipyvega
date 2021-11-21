if ((window as any).require !== undefined) {
  (window as any).require.config({
    map: {
      "*": {
        "jupyter-vega": "nbextensions/jupyter-vega/index",
      },
    },
  });
}
export function load_ipython_extension() {}
