import React from "react";

class PltButton extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "title": null,
      "position": {
        "row": this.props.row_position,
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

    this.state = {"position": this.props.row_position}
  }

  render() {
    return (
      <tr>
        {[1, 2, 3, 4, 5, 6, 7, 8].map((number) =>
          <td>
            <PltButton row_position={this.state.position} col_position={number} key={number}/>
          </td>
        )}
      </tr>
    )
  }
}

class PltWorkSpace extends React.Component {
  render() {
    return (
      <div className={'col mt-5 mt-md-3 mb-3 mx-3'}>
        <table className={"bg-light table-bordered"}>
          <tbody>
          {[1, 2, 3, 4, 5].map((number) =>
            <PltRow row_position={number} key={number}/>
          )}
          </tbody>
        </table>
      </div>
    )
  }
}

export default PltWorkSpace;