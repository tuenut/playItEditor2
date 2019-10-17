import React, {Fragment} from 'react';
import PltWorkSpace from './PltWorkSpace/PltWorkSpace';
import SidePane from '../SidePaneView/SidePane';


export default class MainView extends React.Component {
  render() {
    return (
      <Fragment>
        <SidePane/>
        <PltWorkSpace/>
      </Fragment>
    )
  }
}
