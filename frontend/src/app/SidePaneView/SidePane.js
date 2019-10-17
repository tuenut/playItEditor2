import React, {Fragment} from "react";

import {ProjectContext} from '../Context/ProjectContext';
import ProjectTree from './ProjectTree';


export default class SidePane extends React.Component {
  static contextType = ProjectContext;

  constructor(props) {
    super(props);

    this.state = {
      "style": {
        "height": "100%",
        "marginTop": "4.2rem",
        "position": "fixed",
        "width": "16rem",
        "zIndex": 998,
      },
      "classes": "col border-right border-dark bg-light px-0 overflow-auto"
    }
  }

  render() {
    return (
      <nav className={this.state.classes} style={this.state.style}>
        <div className={"alert-danger w-100 m-0"}>{this.context.projectState.project_name}</div>
        <div className="d-flex flex-column my-3 d-xs-none">
          {this.context.projectState && <ProjectTree tree={this.context.projectState.project_tree} path={[]}/>}
        </div>
      </nav>
    )
  }

}




