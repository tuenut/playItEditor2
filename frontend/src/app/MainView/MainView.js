import React from 'react';
import PltWorkSpace from './PltWorkSpace';
import SidePane from '../SidePaneView/SidePane';

class MainView extends React.Component {
  constructor(props) {
    super(props);

    this.state = {"project": this.props.project};
  }

  render() {
    if (this.props.project !== this.state.project) {
      this.setState({"project": this.props.project});
    }

    return (
      <main role="main">
        <SidePane/>
        <PltWorkSpace project={this.state.project}/>
      </main>
    )
  }
}

export default MainView;