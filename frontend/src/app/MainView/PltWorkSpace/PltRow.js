import React from "react";

import PltButton from "./PltButton";
import {ProjectContext, AppStateContext} from "../../Context/ProjectContext";


export default class PltRow extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "position": this.props.rowPosition,
      "cells": [1, 2, 3, 4, 5, 6, 7, 8]
    }
  }

  loadButton(y, projectState, appState) {
    /*Ищем конфигурацию данной кнопки в контексте исходя из позиции кнопки.
    * todo: найти способ, как не итерироваться по всем кнопкам, а сузить поиск, хотя бы до строки,
    * todo: либо сделать матричную индексацию кнопок в контексте.
    * */

    if (projectState.menu_macros !== null) {
      let position = [this.state.position, y];
      let tree_object = projectState.project_tree;

      for (let i in appState.currentMacros) {
        tree_object = tree_object[appState.currentMacros[i]];
      }
      let macros_object = tree_object;

      let entry_section = macros_object["Entry"];

      let entry_keys = Object.keys(entry_section);

      for (let i in entry_keys) {
        let key = entry_keys[i];
        let key_position = entry_section[key].split(',');

        if (position[0] == key_position[0] && position[1] == key_position[1]) {
          return macros_object[key.toUpperCase()]
        }
      }
    }
  }

  render() {
    return (
      <ProjectContext.Consumer>
        {({projectState}) => (
          <AppStateContext.Consumer>
            {({appState}) => (
              <tr>
                {this.state.cells.map((number) =>
                  <PltButton
                    config={this.loadButton(number, projectState, appState)} key={number}
                    position={[this.state.position, number]}
                  />
                )}
              </tr>
            )}
          </AppStateContext.Consumer>
        )}
      </ProjectContext.Consumer>
    )
  }
}