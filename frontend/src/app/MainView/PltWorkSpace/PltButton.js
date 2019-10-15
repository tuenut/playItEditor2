import React, {Fragment} from "react";
import {ContextMenuTrigger} from "react-contextmenu";

import ProjectContext from '../../Context/ProjectContext';

import PltButtonContextMenu from './PltButtonContextMenu';

function PltButtonTitle(props) {
  let title_lines = props.title ? props.title.split("/n") : [];

  return (
    <Fragment>
      {title_lines.map((text, index) =>
        <div className={"text-center"} key={index}>
          <span>{text}</span>
          <br/>
        </div>
      )}
    </Fragment>
  )
}


export default class PltButton extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "position": this.props.position,
      "div_style": {
        "width": "160px",
        "height": "160px",
      },
      "config": this.props.config ? this.props.config : {
        "bkcolor": null,
        "content": null,
        "id": null,
        "title": null
      }
    };

    this.edit = this.edit.bind(this);
    this.isButtonEmpty = this.isButtonEmpty.bind(this);
    this.setButtonEmpty = this.setButtonEmpty.bind(this);
  }

  isButtonEmpty() {
    let keys = Object.keys(this.state.config)
    for (let i in keys) {
      if (this.state.config[keys[i]] !== null) {
        return false
      }
    }
    return true
  }

  setButtonEmpty() {
    /*Equals operation of delete button.*/
    this.setState({
      "config": {
        "bkcolor": null,
        "content": null,
        "id": null,
        "title": null
      }
    })
  }

  getBgColor() {
    return this.props.config ? {
      "backgroundColor": `rgb(${this.props.config['bkcolor']})`,
      "borderStyle": "outset",
      "borderColor": "#dee2e6",
      "borderWidth": "1px"
    } : {}
  }

  edit(config) {
    this.setState({"config": config})
  }

  handleOnClick(event) {

  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.config) {
      this.setState({"config": nextProps.config});
    } else {
      this.setButtonEmpty();
    }
  }

  static contextType = ProjectContext;

  render() {
    let style = Object.assign(this.getBgColor(), this.state.div_style);

    return (
      <td className={"m-0 p-0"} style={this.state.div_style}>

        <ContextMenuTrigger id={this.state.position.join('')}>
          <button className={"btn rounded-0 m-0 p-0"} style={style} type={"button"} onClick={this.handleOnClick}>
            <PltButtonTitle title={this.props.config && this.props.config['title']}/>
          </button>
        </ContextMenuTrigger>

        <PltButtonContextMenu menuId={this.state.position.join('')} isButtonEmpty={this.isButtonEmpty}/>

      </td>
    )
  }
}