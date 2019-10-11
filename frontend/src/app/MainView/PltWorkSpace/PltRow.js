import React from "react";

import PltButton from "./PltButton";
import ProjectContext from "../../Context/ProjectContext";


export default class PltRow extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "position": this.props.rowPosition,
      "cells": [1, 2, 3, 4, 5, 6, 7, 8]
    }
  }

  static contextType = ProjectContext;

  loadButton(y) {
    /*Ищем конфигурацию данной кнопки в контексте исходя из позиции кнопки.
    * todo: найти способ, как не итерироваться по всем кнопкам, а сузить поиск, хотя бы до строки,
    * todo: либо сделать матричную индексацию кнопок в контексте.
    * */
    if (this.context.project.menu_macros) {
      let position = [this.state.position, y];
      let macros = this.context.project.project_tree[this.context.current_macros];
      let entry_section = macros["Entry"];
      let entry_keys = Object.keys(entry_section);

      for (let i in entry_keys) {
        let key = entry_keys[i];
        let key_position = entry_section[key].split(',');

        if (position[0] == key_position[0] && position[1] == key_position[1]) {
          return macros[key.toUpperCase()]
        }
      }
    }
  }


  render() {
    return (
      <tr>
        {
          this.state.cells.map((number) =>
            <PltButton config={this.loadButton(number)} key={number} position={[this.state.position, number]}/>
          )
        }
      </tr>
    )
  }
}