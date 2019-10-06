import React from "react";

import PltButton from "./PltButton";


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
                {this.props.rowContent && this.props.rowContent[0].path}
                <PltButton rowPosition={this.state.position} col_position={number} key={number}/>
              </td>
          )
        }
      </tr>
    )
  }
}