import React from "react";
import ProjectTreeContainer from '../../../containers/MainView/SidePaneView/ProjectTree';
import ProjectTitleContainer from '../../../containers/MainView/SidePaneView/ProjectTitle';


export default class SidePane extends React.Component {
  render() {
    let style = {
      "height": "100%",
      "marginTop": "4.2rem",
      "position": "fixed",
      "width": "16rem",
      "zIndex": 998,
    };
    let classes = "col border-right border-dark bg-light px-0 overflow-auto";

    return (
      <nav className={classes} style={style}>
        <ProjectTitleContainer/>

        <div className="d-flex flex-column my-3 d-xs-none">
          <ProjectTreeContainer/>
        </div>
      </nav>
    )
  }
}
