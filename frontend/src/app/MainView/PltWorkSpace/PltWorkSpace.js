import React from "react";
import {Table} from 'react-bootstrap';

import PltRow from './PltRow';
import ProjectContext from '../../Context/ProjectContext';


function PltWorkSpaceTitle(props) {
  return (
    <thead>
    <tr className={"border-0"}>
      <td colSpan={8} className={"border-0 p-0 m-0"}>
        <ProjectContext.Consumer>
          {
            (context) =>
              <div className={"alert-danger w-100 m-0"}>
                Editor {context.project && ("<" + context.project.menu_macros + ">")}
              </div>
          }
        </ProjectContext.Consumer>
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
        <Table bordered>
          <PltWorkSpaceTitle/>
          <tbody>
          {this.state.rows_list.map((number) =>
            <PltRow rowPosition={number} key={number}/>
          )}
          </tbody>
        </Table>
      </main>
    )
  }
}

export default PltWorkSpace;