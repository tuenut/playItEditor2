import React from 'react';

import MainView from './MainView/MainView';
import NavigationBar from './TopPaneView/NavigationBar';
import Error from './Modals/Error';
import {ProjectContext, AppMethodsContext, AppStateContext} from './Context/ProjectContext';


export default class App extends React.Component {
  constructor(props) {
    super(props);

    this.openProject = this.openProject.bind(this);
    this.closeErrorModal = this.closeErrorModal.bind(this);
    this.raiseErrorModal = this.raiseErrorModal.bind(this);
    this.switchMacros = this.switchMacros.bind(this);

    this.state = {
      "projectState": {},
      "appMethods": {
        "openProject": this.openProject,
        "raiseError": this.raiseErrorModal,
        "closeError": this.closeErrorModal,
        "switchMacros": this.switchMacros
      },
      "appState": {
        "currentMacros": null,
        "error": {
          "show": false,
          "title": null,
          "body": null,
        }
      }
    };
  }

  switchMacros(macros_name) {
    this.setState({
      "appState": {
        "currentMacros": macros_name,
        "error": this.state.appState.error
      }
    })
  }

  openProject(project_json) {
    this.setState({
      "projectState": project_json,
      "appState": {
        "currentMacros": project_json.menu_macros,
        "error": this.state.appState.error
      }
    });

    // console.log(this.state);
  }

  closeErrorModal() {
    this.setState({
      "appState": {
        "currentMacros": this.state.appState.currentMacros,
        "error": {
          "show": false,
          "title": null,
          "body": null,
        }
      }
    })
  }

  raiseErrorModal(title, body) {
    this.setState({
      "appState": {
        "error": {
          "show": true,
          "title": title,
          "body": body
        }
      }
    })
  }

  render() {
    return (
      <div className={"container-fluid"}>
        <div className={"row flex-xl-nowrap"}>

          <ProjectContext.Provider value={{"projectState": this.state.projectState}}>
            <AppMethodsContext.Provider value={{"appMethods": this.state.appMethods}}>
              <AppStateContext.Provider value={{"appState": this.state.appState}}>

                <NavigationBar/>

                <MainView/>

                <Error/>

              </AppStateContext.Provider>
            </AppMethodsContext.Provider>
          </ProjectContext.Provider>

        </div>
      </div>
    )
  }
}

