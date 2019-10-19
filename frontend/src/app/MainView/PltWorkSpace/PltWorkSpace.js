import React, {Fragment} from "react";

import PltButton from "./PltButton";
import {ProjectContext, AppMethodsContext, AppStateContext} from '../../Context/ProjectContext';


export default class PltWorkSpace extends React.Component {
  static contextType = ProjectContext;

  constructor(props) {
    super(props);

    this.state = {
      "mainStyle": {
        "marginTop": "7rem",
        "marginLeft": "16rem",
        "zIndex": 0
      },
    }
  }

  loadButton(row, col, currentMacros) {
    /*Ищем конфигурацию данной кнопки в контексте исходя из позиции кнопки.
    * todo: найти способ, как не итерироваться по всем кнопкам, а сузить поиск, хотя бы до строки,
    * todo: либо сделать матричную индексацию кнопок в контексте.
    * */
    let tree_object = this.getCurrentMacrosConfig(currentMacros);

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

  getCurrentMacrosConfig(currentMacros) {
    let tree_object = this.context.projectState.project_tree;

    for (let i in currentMacros) {
      tree_object = tree_object[currentMacros[i]];
    }

    return tree_object
  }

  render() {
    return (
      <main role="main" className={"col"} style={this.state.mainStyle}>
        <AppStateContext.Consumer>
          {({appState}) => (appState.currentMacros &&

            <table className={"table-bordered"}>
              <tbody>
              {[1, 2, 3, 4, 5].map((row) =>
                <tr key={row}>
                  {[1, 2, 3, 4, 5, 6, 7, 8].map((col) =>
                    <td className={"m-0 p-0"}>
                      <PltButton
                        config={this.loadButton(row, col, appState.currentMacros)} key={`${row}.${col}`}
                        position={[row, col]}
                      />
                    </td>
                  )}
                </tr>
              )}
              </tbody>
            </table>

          )}
        </AppStateContext.Consumer>
      </main>
    )
  }
}



