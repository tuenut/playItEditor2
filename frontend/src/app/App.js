import React from 'react';

import MainView from './MainView/MainView';
import NavigationBar from './TopPaneView/NavigationBar';
import Error from './Modals/Error';
import ProjectContext from './Context/ProjectContext';


class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "project": null,
      "error": {
        "show": false,
        "title": null,
        "body": null,
      }
    };

    this.openProject = this.openProject.bind(this);
    this.closeErrorModal = this.closeErrorModal.bind(this);
    this.raiseErrorModal = this.raiseErrorModal.bind(this);
  }

  openProject(project_json) {
    this.setState({"project": project_json});

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
    const context = {
      "project": this.state.project,
      "openProjectCallback": this.openProject,
      "raiseErrorCallback": this.raiseErrorModal,
      "closeErrorCallback": this.closeErrorModal
    };

    const error = this.state.error

    return (
      <div className={"container-fluid"}>

        <div className={"row flex-xl-nowrap"}>

          <ProjectContext.Provider value={context}>

            <NavigationBar/>

            <MainView/>

            <Error closeCallback={this.closeErrorModal} error={error}/>

          </ProjectContext.Provider>

        </div>
      </div>
    )
  }
}


export default App;
