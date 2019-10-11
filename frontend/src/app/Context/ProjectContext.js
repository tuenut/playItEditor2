import React from "react";

const ProjectContext = React.createContext({
  project: {},
  loadProject: () => {}
});

export default ProjectContext;