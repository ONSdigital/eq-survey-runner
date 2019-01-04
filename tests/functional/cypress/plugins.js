// ***********************************************************
// This example plugins/index.js can be used to load plugins
//
// You can change the location of this file or turn off loading
// the plugins file with the 'pluginsFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/plugins-guide
// ***********************************************************

// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)
const webpack = require('@cypress/webpack-preprocessor')

module.exports = (on, config) => {
  // Using the webpack preprocessor allows us to use require.context to include
  // all files in a directory. The default is browserify which doesn't have that
  // option
  on('file:preprocessor', webpack())
}

