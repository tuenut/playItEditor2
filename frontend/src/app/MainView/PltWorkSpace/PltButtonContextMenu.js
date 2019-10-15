import React, {Fragment} from "react";
import {ContextMenu, MenuItem, ContextMenuTrigger} from "react-contextmenu";
import {Card, ListGroup, ListGroupItem} from "react-bootstrap";


export default class PltButtonContextMenu extends React.Component {
  render() {
    return (
      <ContextMenu id={this.props.menuId}>
        <Card>
          <ListGroup>
            {
              this.props.isButtonEmpty() ? (
                <ListGroup.Item>
                  <MenuItem data={{}} onClick={this.props.edit}>
                    Создать
                  </MenuItem>
                </ListGroup.Item>
              ) : (
                <Fragment>
                  <ListGroup.Item>
                    <MenuItem data={{}} onClick={this.props.edit}>
                      Редактировать
                    </MenuItem>
                  </ListGroup.Item>
                  <ListGroup.Item>
                    <MenuItem data={{}} onClick={this.props.delete}>
                      Удалить
                    </MenuItem>
                  </ListGroup.Item>
                </Fragment>
              )
            }

          </ListGroup>
        </Card>
      </ContextMenu>
    )
  }
}
