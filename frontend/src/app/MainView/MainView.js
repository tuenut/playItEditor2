import React, {Fragment} from 'react';
import PltWorkSpace from './PltWorkSpace/PltWorkSpace';
import SidePane from '../SidePaneView/SidePane';


export default MainView;

function MainView() {
  return (
    <Fragment>
      <SidePane/>
      <PltWorkSpace/>
    </Fragment>
  )
}
