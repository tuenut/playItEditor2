import React, {Fragment} from 'react';
import PltWorkSpace from './PltWorkSpace/PltWorkSpace';
import SidePane from '../SidePaneView/SidePane';
import ProjectContext from "../Context/ProjectContext";

class MainView extends React.Component {
  static contextType = ProjectContext;

  render() {
    return (
      <Fragment>
        <SidePane/>
        {this.context.current_macros && <PltWorkSpace/>}
      </Fragment>
    )
  }
}

export default MainView;