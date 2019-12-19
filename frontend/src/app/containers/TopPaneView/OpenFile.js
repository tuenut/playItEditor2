import React from "react";
import { connect } from "react-redux";

import OpenFile from "../../components/TopPaneView/OpenFile";
import {changeFilePath} from "../../store/App/TopPaneView/OpenFile/actions";
import {openProject} from "../../store/App/actions"

class OpenFileContainer extends React.Component {
  render(){
    return(
      <OpenFile
        changeFilePath={this.props.changeFilePath} open_project_path={this.props.open_project_path}
        openProject={this.props.openProject}
      />
    )
  }
}

const mapStateToProps = state => {
  return{
    open_project_path: state.navbar.open_project_path,
  }
};

const mapDispatchToProps = {
  changeFilePath,
  openProject
};

export default connect(mapStateToProps, mapDispatchToProps)(OpenFileContainer);
