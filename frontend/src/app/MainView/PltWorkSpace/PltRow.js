import React from "react";

import PltButton from "./PltButton";
import ProjectContext from '../../Context/ProjectContext';


function finder(context) {


}


export default class PltRow extends React.Component {
  constructor(props) {
    super(props);

    this.state = {"position": this.props.rowPosition, "cells_list": [1, 2, 3, 4, 5, 6, 7, 8]}
  }

  render() {
    return (
      <tr>
        {
          this.state.cells_list.map(
            (number) =>
              <td key={number}>

                <ProjectContext.Consumer>
                  {
                    (context) =>
                      <PltButton
                        rowPosition={this.state.position} col_position={number} key={number}
                        content={
                          context.project && (
                            () => context.project.project_tree[context.project.menu_macros[1]])
                        }
                      />
                  }
                </ProjectContext.Consumer>

              </td>
          )
        }
      </tr>
    )
  }
}