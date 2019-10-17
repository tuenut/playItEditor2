import React from "react";

const ProjectContext = React.createContext({"projectState": {}});
const AppMethodsContext = React.createContext({
  "appMethods": {
    "openProject": () => {},
    "raiseError": () => {},
    "closeError": () => {},
    "switchMacros": () => {}
  }
});
const AppStateContext = React.createContext({"appState": {}});

export {ProjectContext, AppMethodsContext, AppStateContext};