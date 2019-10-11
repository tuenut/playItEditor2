import React from "react";

import ProjectContext from '../../Context/ProjectContext';


export default class PltButton extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "position": this.props.position,
      "div_style": {
        "width": "160px",
        "height": "160px",
      }
    };
  }

  getBgColor() {
    return this.props.config ? {
      "backgroundColor": `rgb(${this.props.config['bkcolor']})`,
      "borderStyle": "outset",
      "borderColor": "#dee2e6",
      "borderWidth": "1px"
    } : {}
  }

  static contextType = ProjectContext;

  render() {
    let style = Object.assign(this.getBgColor(), this.state.div_style);

    return (
      <td className={"m-0 p-0"}>
        <div className={""} style={style}>
          {this.props.config && this.props.config['title'].split("/n").map(
            (text, index) => <div className={"text-center"} key={index}><span>{text}</span><br/></div>
          )}
        </div>
      </td>
    )
  }
}