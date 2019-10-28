import React from "react";

const ProjectContext = React.createContext({"projectState": {}});
const AppMethodsContext = React.createContext({
  "appMethods": {

    "openProject": () => {},
    "raiseErrorModal": () => {},
    "closeErrorModal": () => {},
    "switchMacros": () => {},
    "closeEditPltButtonModal": () => {},
    "openEditPltButtonModal": () => {}
  }
});
const AppStateContext = React.createContext({"appState": {}});

export {ProjectContext, AppMethodsContext, AppStateContext};