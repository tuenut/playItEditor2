import React, {Fragment} from "react";

import PltRow from './PltRow';
import {ProjectContext, AppMethodsContext, AppStateContext} from '../../Context/ProjectContext';


export default class PltWorkSpace extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "rowsList": [1, 2, 3, 4, 5],
      "classes": "col",
      "styles": {"marginTop": "7rem", "marginLeft": "16rem", "zIndex": 0}
    }
  }

  render() {
    return (
      <main role="main" className={this.state.classes} style={this.state.styles}>
        <AppStateContext.Consumer>
          {({appState}) => (
            appState.currentMacros && <PltEditorTable rows={this.state.rowsList}/>
          )}
        </AppStateContext.Consumer>
      </main>
    )
  }
}


function PltEditorTable(props) {
  return (
    <table className={"table-bordered"}>
      <tbody>
      {props.rows.map((number) => <PltRow rowPosition={number} key={number}/>)}
      </tbody>
    </table>
  )
}


