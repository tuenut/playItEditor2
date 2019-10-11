import React from 'react';

import MainView from './MainView/MainView';
import NavigationBar from './TopPaneView/NavigationBar';
import Error from './Modals/Error';
import ProjectContext from './Context/ProjectContext';


class App extends React.Component {
  constructor(props) {
    super(props);

    this.openProject = this.openProject.bind(this);
    this.closeErrorModal = this.closeErrorModal.bind(this);
    this.raiseErrorModal = this.raiseErrorModal.bind(this);
    this.switchMacros = this.switchMacros.bind(this);

    this.state = {
      "project": {},
      "current_macros": null,
      "openProject": this.openProject,
      "error": {
        "show": false,
        "title": null,
        "body": null,
      },
      "raiseError": this.raiseErrorModal,
      "closeError": this.closeErrorModal,
      "switchMacros": this.switchMacros
    };
  }

  switchMacros(macros_name){
    this.setState({"current_macros": macros_name})
  }

  openProject(project_json) {
    this.setState({"project": project_json});
    this.switchMacros(this.state.project.menu_macros[1]); // open default macros

    console.log(this.state.project)
  }

  closeErrorModal() {
    this.setState({
      "error": {
        "show": false,
        "title": null,
        "body": null,
      }
    })
  }

  raiseErrorModal(title, body) {
    this.setState({
      "error": {
        "show": true,
        "title": title,
        "body": body
      }
    })
  }

  render() {
    return (
      <div className={"container-fluid"}>

        <div className={"row flex-xl-nowrap"}>

          <ProjectContext.Provider value={this.state}>

            <NavigationBar/>

            <MainView/>

            <Error error={this.state.error}/>

          </ProjectContext.Provider>

        </div>
      </div>
    )
  }
}


export default App;
