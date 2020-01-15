import {connect} from "react-redux";

import OpenFile from "../../components/TopPaneView/OpenFile";
import {projectPathOnChange} from "../../store/App/TopPaneView/OpenFile/actions";
import {openProjectOnClick} from "../../store/App/actions"


const mapStateToProps = state => {
  return {
    project_path: state.navbar.project_path,
  }
};

const mapDispatchToProps = {
  projectPathOnChange: projectPathOnChange,
  openProjectOnClick: openProjectOnClick
};

export default connect(mapStateToProps, mapDispatchToProps)(OpenFile);
