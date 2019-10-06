import React from 'react';

import MainView from './MainView/MainView';
import NavigationBar from './TopPaneView/NavigationBar';
import ProjectContext from './Context/ProjectContext';


class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {"project": null};

    this.openProject = this.openProject.bind(this);
  }

  openProject(project_json) {
    this.setState({"project": project_json});

    console.log(this.state.project)
  }

  render() {
    return (
      <div className={"container-fluid"}>
        <div className={"row flex-xl-nowrap"}>

          <ProjectContext.Provider value={{"project": this.state.project, "openProjectCallback": this.openProject}}>

            <NavigationBar/>

            <MainView/>

          </ProjectContext.Provider>

        </div>
      </div>
    )
  }
}


export default App;
