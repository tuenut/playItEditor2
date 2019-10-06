import React from 'react';
import MainView from './MainView/MainView';
import NavigationBar from './TopPaneView/NavigationBar';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {"project": null};

    this.openProject = this.openProject.bind(this);
  }

  openProject(project_json) {
    this.setState({"project": project_json});
  }

  render() {
    let project_name = this.state.project ? (this.state.project.project_name) : (this.state.project);

    console.log(this.state.project);

    return (
      <div className="container-fluid">
        <div className={"row flex-xl-nowrap"}>
          <NavigationBar openProjectCallback={this.openProject} projectName={project_name}/>
          <MainView project={this.state.project}/>
        </div>
      </div>
    )
      ;
  }
}

export default App;
