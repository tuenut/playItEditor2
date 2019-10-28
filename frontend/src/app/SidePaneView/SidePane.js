import React from "react";

import {ProjectContext} from '../Context/ProjectContext';
import ProjectTree from './ProjectTree';


export default SidePane;

function SidePane() {
  let style = {
    "height": "100%",
    "marginTop": "4.2rem",
    "position": "fixed",
    "width": "16rem",
    "zIndex": 998,
  };
  let classes = "col border-right border-dark bg-light px-0 overflow-auto";

  return (
    <ProjectContext.Consumer>
      {({projectState}) => (

        <nav className={classes} style={style}>
          <div className={"alert-danger w-100 m-0"}>{projectState.project_name}</div>
          <div className="d-flex flex-column my-3 d-xs-none">
            {projectState && <ProjectTree tree={projectState.project_tree} path={[]}/>}
          </div>
        </nav>

      )}
    </ProjectContext.Consumer>
  )
}
