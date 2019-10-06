import React from "react";

import ProjectContext from '../../Context/ProjectContext';


export default class PltButton extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "title": null,
      "position": {
        "row": this.props.rowPosition,
        "col": this.props.col_position
      }
    }
  }

  render() {
    return (
      <div className={"d-block"} style={{"width": "160px", "height": "160px"}}>
      </div>
    )
  }
}