import React from "react";

class PltButton extends React.Component {
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

class PltRow extends React.Component {
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
              <td>
                {this.props.rowContent && this.props.rowContent[0].path}
                <PltButton rowPosition={this.state.position} col_position={number} key={number}/>
              </td>
          )
        }
      </tr>
    )
  }
}

class PltWorkSpace extends React.Component {
  constructor(props) {
    super(props);

    this.state = {"rows_list": [1, 2, 3, 4, 5], "project": this.props.project}
  }

  render() {
    if (this.props.project !== this.state.project) {
      this.setState({"project": this.props.project});
    }

    return (
      <div className="col-12 col-md-9 col-xl-8" style={{"margin-top": "7rem", "margin-left": "16rem", "zIndex": 0}}>
        <table className={"bg-light table-bordered"}>
          <tbody>
          {
            this.state.rows_list.map(
              (number) => {
                console.log("project: " + this.state.project);

                let content = this.state.project && this.state.project.macroses;

                console.log("content: " + content);

                return <PltRow rowPosition={number} key={number} rowContent={content}/>
              })
          }
          </tbody>
        </table>
      </div>
    )
  }
}

export default PltWorkSpace;