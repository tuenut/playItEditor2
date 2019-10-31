import React from 'react';

import MainView from './MainView/MainView';
import NavigationBar from './TopPaneView/NavigationBar';
import ErrorModal from './Modals/Error';
import EditPltButtonModalView from './Modals/EditButton';

import {ProjectContext, AppMethodsContext, AppStateContext} from './Context/ProjectContext';


class App extends React.Component {
  constructor(props) {
    super(props);

    this.openProject = this.openProject.bind(this);
    this.closeErrorModal = this.closeErrorModal.bind(this);
    this.raiseErrorModal = this.raiseErrorModal.bind(this);
    this.switchMacros = this.switchMacros.bind(this);
    this.openEditPltButtonModal = this.openEditPltButtonModal.bind(this);
    this.closeEditPltButtonModal = this.closeEditPltButtonModal.bind(this);
    this.getButton = this.getButton.bind(this);
    this.getMacros = this.getMacros.bind(this);

    this.state = {
      "projectState": {},
      "appMethods": {
        "openProject": this.openProject,
        "raiseErrorModal": this.raiseErrorModal,
        "closeErrorModal": this.closeErrorModal,
        "switchMacros": this.switchMacros,
        "closeEditPltButtonModal": this.closeEditPltButtonModal,
        "openEditPltButtonModal": this.openEditPltButtonModal,
        "getButton": this.getButton,
        "getMacros": this.getMacros
      },
      "appState": {
        "currentMacros": null,
        "error": {
          "show": false,
          "title": null,
          "body": null,
        },
        "edit": {
          "show": false,
          "button": null
        }
      }
    };
  }

  switchMacros(macros_name) {
    this.setState({
      "appState": {
        "currentMacros": macros_name,
        "error": this.state.appState.error,
        "edit": this.state.appState.edit,
      }
    })
  }

  openProject(project_json) {
    this.setState({
      "projectState": project_json,
      "appState": {
        "currentMacros": project_json.menu_macros,
        "error": this.state.appState.error,
        "edit": this.state.appState.edit,
      }
    });
  }

  closeErrorModal() {
    this.setState({
      "appState": {
        "currentMacros": this.state.appState.currentMacros,
        "edit": this.state.appState.edit,
        "error": {
          "show": false,
          "title": null,
          "body": null,
        }
      }
    })
  }

  closeEditPltButtonModal() {
    this.setState({
      "appState": {
        "currentMacros": this.state.appState.currentMacros,
        "error": this.state.appState.error,
        "edit": {
          "show": false,
          "button": null
        }
      }
    })
  }

  openEditPltButtonModal(btnPosition) {
    let btnPositionArray = btnPosition.split('x');
    let row = btnPositionArray[0];
    let col = btnPositionArray[1];
    let button = this.getButton(row, col, this.state.appState.currentMacros);

    this.setState({
      "appState": {
        "currentMacros": this.state.appState.currentMacros,
        "error": this.state.appState.error,
        "edit": {
          "show": true,
          "button": button,
        }
      }
    })
  }

  raiseErrorModal(title, body) {
    this.setState({
      "appState": {
        "currentMacros": this.state.appState.currentMacros,
        "edit": this.state.appState.edit,
        "error": {
          "show": true,
          "title": title,
          "body": body
        }
      }
    })
  }


  getButton(row, col, macros) {
    /*Ищем конфигурацию данной кнопки в контексте исходя из позиции кнопки.
    * todo: найти способ, как не итерироваться по всем кнопкам, а сузить поиск, хотя бы до строки,
    * todo: либо сделать матричную индексацию кнопок в контексте.
    * */
    let tree_object = this.getMacros(macros);

    let entry_section = tree_object["Entry"];
    let entry_keys = Object.keys(entry_section);

    for (let i in entry_keys) {
      let key = entry_keys[i];
      let key_position = entry_section[key].split(',');

      if (row == key_position[0] && col == key_position[1]) {
        return tree_object[key.toUpperCase()]
      }
    }
  }

  getMacros(macros) {
    let tree_object = this.state.projectState.project_tree;

    for (let i in macros) {
      tree_object = tree_object[macros[i]];
    }

    return tree_object
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

                <ErrorModal/>
                <EditPltButtonModalView/>

              </AppStateContext.Provider>
            </AppMethodsContext.Provider>
          </ProjectContext.Provider>

        </div>
      </div>

    )
  }
}

export default App;
