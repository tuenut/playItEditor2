import React from 'react';
import PltWorkSpace from './PltWorkSpace/PltWorkSpace';
import SidePane from '../SidePaneView/SidePane';

class MainView extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <main role="main">
        <SidePane/>
        <PltWorkSpace/>
      </main>
    )
  }
}

export default MainView;