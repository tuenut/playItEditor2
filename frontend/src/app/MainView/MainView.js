import React, {Fragment} from 'react';
import PltWorkSpace from './PltWorkSpace/PltWorkSpace';
import SidePane from '../SidePaneView/SidePane';

class MainView extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Fragment>
        <SidePane/>
        <PltWorkSpace/>
      </Fragment>
    )
  }
}

export default MainView;