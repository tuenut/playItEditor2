import React from 'react';
import MainView from './MainView/MainView';
import NavigationBar from './TopPaneView/NavigationBar';
import SidePane from './SidePaneView/SidePane';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {"project": {}};

    this.openProject =this.openProject.bind(this);
  }

  openProject(project_json){
    this.setState({"project": project_json});
  }

  render() {
    return (
      <div className="container-fluid">
        <div className={"row flex-xl-nowrap"}>
          <NavigationBar openProjectCallback={this.openProject} projectName={this.state.project.project_name}/>
          <SidePane/>
          <MainView/>
        </div>
      </div>
    )
      ;
  }
}

export default App;
