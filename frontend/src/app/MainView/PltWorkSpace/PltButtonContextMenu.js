import React, {Fragment} from "react";
import {ContextMenu, MenuItem} from "react-contextmenu";
import {Card, Button, ButtonGroup} from "react-bootstrap";

import {AppMethodsContext} from '../../Context/ProjectContext';


export default class PltButtonContextMenu extends React.Component {
  static contextType = AppMethodsContext;

  constructor(props) {
    super(props);

    this.handleOpenEditView = this.handleOpenEditView.bind(this);
    this.handlDeleteButton = this.handlDeleteButton.bind(this);
  }

  handleOpenEditView() {
    this.context.appMethods.openEditPltButtonModal(this.props.menuId);
  }

  handlDeleteButton() {

  }

  render() {
    return (
      <ContextMenu id={this.props.menuId}>
        <Card>
          <ButtonGroup vertical>

            {this.props.isButtonEmpty() ? (
              <MenuItem data={{}} onClick={this.handleOpenEditView}>
                <Button variant="light">
                  Создать
                </Button>
              </MenuItem>
            ) : (
              <Fragment>
                <Button variant="light">
                  <MenuItem data={{}} onClick={this.handleOpenEditView}>
                    Редактировать
                  </MenuItem>
                </Button>

                <Button variant="light">
                  <MenuItem data={{}} onClick={this.handlDeleteButton}>
                    Удалить
                  </MenuItem>
                </Button>
              </Fragment>
            )}

          </ButtonGroup>
        </Card>
      </ContextMenu>
    )
  }
}
