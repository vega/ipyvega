// This file contains the javascript that is run when the notebook is loaded.
// It contains some requirejs configuration and the `load_ipython_extension`
// which is required for any notebook extension.
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
const dataBaseURL = document.querySelector('body').getAttribute('data-base-url');
__webpack_public_path__ = `${dataBaseURL}nbextensions/jupyter-vega`;


// Configure requirejs
if (window.require) {
  window.require.config({
    map: {
      "*": {
        "jupyter-vega": "nbextensions/jupyter-vega/index",
      }
    }
  });
}