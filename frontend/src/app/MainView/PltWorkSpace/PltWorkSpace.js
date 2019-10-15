import React from "react";

import PltRow from './PltRow';
import ProjectContext from '../../Context/ProjectContext';


function PltWorkSpaceTitle(props) {
  return (
    <thead>
    <tr className={"border-0"}>
      <td colSpan={8} className={"border-0 p-0 m-0"}>

        <div className={"alert-danger w-100 m-0"}>
          Editor {("<" + props.title.join('/') + ">")}
        </div>

      </td>
    </tr>
    </thead>
  )
}


class PltWorkSpace extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "rows_list": [1, 2, 3, 4, 5],
      "classes": "col",
      "styles": {"marginTop": "7rem", "marginLeft": "16rem", "zIndex": 0}
    }
  }

  static contextType = ProjectContext;

  render() {
    return (
      <main role="main" className={this.state.classes} style={this.state.styles}>
        <table className={"table-bordered"}>
          <PltWorkSpaceTitle title={this.context.current_macros}/>
          <tbody>
          {this.state.rows_list.map((number) =>
            <PltRow rowPosition={number} key={number}/>
          )}
          </tbody>
        </table>
      </main>
    )
  }
}

export default PltWorkSpace;

